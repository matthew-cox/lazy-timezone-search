**Last Updated: 2019-01-26 09:28 @matthew-cox**

Table of Contents
=================
  * [Lazy TimeZone Search (ltzs)](#lazy-timezone-search-ltzs)
    * [Requirements](#requirements)
    * [Local Development](#local-development)
      * [Configure Local Python Virtualenv](#configure-local-python-virtualenv)
        * [macOS Fast Setup with Brew](#macos-fast-setup-with-brew)
        * [Pyenv + Virtualenv](#pyenv--virtualenv)
      * [Run the Code Locally](#run-the-code-locally)

# Lazy TimeZone Search (ltzs)

Quick and dirty geocoding and timezone search.

Only tested with Python 3.6.6

## Requirements

Nonstandard packages:

* geopy
* numpy
* pytz
* tzwh

For fast local dev setup, you will need a  Python + Pyenv + Virtualenv.

## Local Development

### Configure Local Python Virtualenv

#### macOS Fast Setup with Brew

If you are on macOS and already have [Homebrew](https://brew.sh) installed, I've included a setup script.

*Note:* This script will install or upgrade pyenv and pyenv-virtualenv. Also, the virtualenv will be available when entering the directory, but not when executing the script from $PATH.

<details>
    <summary><code>./pyenv_setup.sh</code></summary>

    NOTE: Desired Python version is '3.6.6'...
    NOTE: Pyenv name is 'lazy-timezone-search-3.6'...
    NOTE: Upgrading pyenv...
    Updated 1 tap (homebrew/cask).
    No changes to formulae.
    Error: pyenv 1.2.9 already installed
    SUCCESS: done
    NOTE: Python '3.6.6' is already installed.
    NOTE: Pyenv 'lazy-timezone-search-3.6' already exists.
    NOTE: Upgrading pip and setuptools...
    Requirement already up-to-date: pip in ${HOME}/.pyenv/versions/3.6.6/envs/lazy-timezone-search-3.6/lib/python3.6/site-packages (18.1)
    Requirement already up-to-date: setuptools in ${HOME}/.pyenv/versions/3.6.6/envs/lazy-timezone-search-3.6/lib/python3.6/site-packages (40.6.3)
    SUCCESS: done
    NOTE: Installing local dev requirements...
    Requirement already satisfied: geopy in ${HOME}/.pyenv/versions/3.6.6/envs/lazy-timezone-search-3.6/lib/python3.6/site-packages (from -r ${HOME}/Devel/lazy-timezone-search/requirements.txt (line 1)) (1.18.1)
    Requirement already satisfied: numpy in ${HOME}/.pyenv/versions/3.6.6/envs/lazy-timezone-search-3.6/lib/python3.6/site-packages (from -r ${HOME}/Devel/lazy-timezone-search/requirements.txt (line 3)) (1.16.0)
    Requirement already satisfied: pytz in ${HOME}/.pyenv/versions/3.6.6/envs/lazy-timezone-search-3.6/lib/python3.6/site-packages (from -r ${HOME}/Devel/lazy-timezone-search/requirements.txt (line 4)) (2018.9)
    Requirement already satisfied: tzwhere in ${HOME}/.pyenv/versions/3.6.6/envs/lazy-timezone-search-3.6/lib/python3.6/site-packages (from -r ${HOME}/Devel/lazy-timezone-search/requirements.txt (line 5)) (3.0.3)
    Requirement already satisfied: geographiclib<2,>=1.49 in ${HOME}/.pyenv/versions/3.6.6/envs/lazy-timezone-search-3.6/lib/python3.6/site-packages (from geopy->-r ${HOME}/Devel/lazy-timezone-search/requirements.txt (line 1)) (1.49)
    Requirement already satisfied: shapely in ${HOME}/.pyenv/versions/3.6.6/envs/lazy-timezone-search-3.6/lib/python3.6/site-packages (from tzwhere->-r ${HOME}/Devel/lazy-timezone-search/requirements.txt (line 5)) (1.6.4.post2)
    SUCCESS: done

</details><br />

#### Pyenv + Virtualenv

    # install newish python 3.6.x
    $ pyenv install $(cat PYTHON_VERSION)

    # create a repo specific virtualenv
    $ pyenv virtualenv $(cat PYTHON_VERSION) ltzs-$(cat PYTHON_VERSION)

    # switch to the new virtualenv
    $ pyenv local ltzs-$(cat PYTHON_VERSION)

    # ensure that pip and setuptools are new
    $ pip install --upgrade pip setuptools

    # install all the requirements
    $ pip install -r ./requirements.txt
    ...

### Run the Code Locally

Once the requirements are met, one can execute the code locally by running the following:

<details>
    <summary><code>./ltzs.py --help</code></summary>

    usage: ltzs.py [-h] [-l {debug,info,warning,error,critical}] [city]

    Lazy TimeZone Search - Output timezone information about a provided city

    positional arguments:
      city                  Find the timezone of this city

    optional arguments:
      -h, --help            show this help message and exit
      -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                            Logging verbosity. Default: WARNING

</details><br />

Here's an example:

<details>
    <summary><code>./ltzs.py Sedona</code></summary>

    Current timezone: CET
    Sedona timezone: PST

    CET - 2019-01-17 16:49
    UTC - 2019-01-17 15:49
    PST - 2019-01-17 07:49

</details><br />
