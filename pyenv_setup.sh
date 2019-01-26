#!/usr/bin/env bash
#
set -o errexit -o pipefail -o nounset
# set -x
MYDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd -P)
readonly PROJECT_NAME=$(basename "${MYDIR}")
readonly PY_VER_FILE="${MYDIR}/PYTHON_VERSION"
#
##############################################################################
#
# Error message to STDERR
#
puterr() {
    msg="$1"
    >&2 echo -e "\e[31mERROR:\e[39m $msg"
}

export -f puterr
#
##############################################################################
#
# INFO message to STDOUT
#
putinfo() {
  msg="$1"
  echo -e "\e[34mNOTE:\e[39m $msg"
}

export -f putinfo
#
##############################################################################
#
# SUCCESS message to STDOUT
#
putsuccess() {
  msg="$1"
  echo -e "\e[32mSUCCESS:\e[39m $msg"
}

export -f putsuccess
#
##############################################################################
#
if [[ "$(uname -s)" != "Darwin" ]]; then
    puterr "I can only run on macOS!"
    exit 6
fi

if [[ -r "${PY_VER_FILE}" ]]; then
    readonly PY_VER=$(cat "${PY_VER_FILE}")
else
    puterr "Directory is not configured with $(basename "${PY_VER_FILE}") file!"
    exit 7
fi
putinfo "Desired Python version is '${PY_VER}'..."
readonly PY_MAJOR_VER="$(echo "${PY_VER}" | cut -d'.' -f1-2)"

if [[ -r "${MYDIR}/.python-version" ]]; then
    PY_ENV_NAME=$(cat "${MYDIR}/.python-version")
else
    PY_ENV_NAME="${PROJECT_NAME}-${PY_MAJOR_VER}"
fi
putinfo "Pyenv name is '${PY_ENV_NAME}'..."

if command -v brew >/dev/null 2>&1; then

    if command -v pyenv >/dev/null 2>&1; then

        # Update Pyenv
        putinfo "Upgrading pyenv..."
        set +o errexit
        brew update && brew upgrade pyenv
        set -o errexit
        putsuccess "done"

        readonly PYENV_INFO=$(pyenv versions | sed 's/^\([ \t\*]*\)//' | awk '{print $1}')
        set +o errexit +o pipefail
        PY_VERSION_INSTALLED=$(echo "${PYENV_INFO}" | grep -c "^${PY_VER}$")
        set -o errexit -o pipefail

        if [[ $PY_VERSION_INSTALLED -eq 0 ]]; then

            # install requested python
            putinfo "Installing Python '${PY_VER}'..."
            pyenv install "${PY_VER}"
            putsuccess "done"
        else
            putinfo "Python '${PY_VER}' is already installed."
        fi

        set +o errexit +o pipefail
        PY_ENV_INSTALLED=$(echo "${PYENV_INFO}" | grep -c "^${PY_ENV_NAME}$")
        set -o errexit -o pipefail

        if [[ $PY_ENV_INSTALLED -eq 0 ]]; then
            # create a repo specific virtualenv
            putinfo "Creating Pyenv '${PY_ENV_NAME}'..."
            pyenv virtualenv "${PY_VER}" "${PY_ENV_NAME}"
            putsuccess "done"
        else
            putinfo "Pyenv '${PY_ENV_NAME}' already exists."
        fi

        # switch to the new virtualenv
        pyenv local "${PY_ENV_NAME}"

        # ensure that pip and setuptools are new
        putinfo "Upgrading pip and setuptools..."
        pip install --upgrade pip setuptools
        putsuccess "done"

        # install all the requirements
        if [[ -r "${MYDIR}/requirements.txt" ]]; then
            putinfo "Installing local dev requirements..."
            pip install -r "${MYDIR}/requirements.txt"
            putsuccess "done"
        fi

        if [[ -r "${MYDIR}/lambda_function/requirements.txt" ]]; then
          putinfo "Installing lambda function requirements..."
          pip install -r "${MYDIR}/lambda_function/requirements.txt"
          putsuccess "done"
        fi

    else
        puterr "Unable to find pyenv: have you configured your environment?"
    fi
else
    puterr "Unable to find brew: have you configured your environment?"
fi
