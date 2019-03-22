#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
Lazy TimeZone Search - Output timezone information about a provided city
"""
#
# Standard Imports
#
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
from datetime import datetime
import logging
from pathlib import Path
import os
#
# Non-standard imports
#
from geopy.geocoders import Photon
import pytz
from tzlocal import get_localzone
from tzwhere import tzwhere
#
##############################################################################
#
# Reserved environment variables and their defaults
#
DEFAULT_LOG_LEVEL = os.environ.get('PYTHON_LOG_LEVEL', 'WARNING')
#
##############################################################################
#
# Global variables
#
DESCRIPTION = "Lazy TimeZone Search - Output timezone information about a provided city"

CITIES = {
    'boston': (42.3572699, -71.0603766),
    'denver': (39.76185, -104.881105),
    'san francisco': (37.783333, -122.416667),
    'rome': (41.9, 12.5)
}


#
##############################################################################
#
# _get_logger()
#
def _get_logger():
    """
    Reusable code to get the correct logger by name of current file

    Returns:
        logging.logger: Instance of logger for name of current file
    """
    return logging.getLogger(Path(__file__).resolve().name)


#
##############################################################################
#
# handle_arguments()
#
def handle_arguments():
    """
    Handle CLI arguments

    Returns:
        parser.Namespace: Representation of the parsed arguments
    """
    #
    # Handle CLI args
    #
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    # add arguments
    parser.add_argument('-l', '--log-level', action='store', required=False,
                        choices=["debug", "info", "warning", "error", "critical"],
                        default=DEFAULT_LOG_LEVEL,
                        help='Logging verbosity. Default: %(default)s')

    parser.add_argument('-t', '--time-only', action='store_true', required=False,
                        help='Show time only. Default: %(default)s')

    parser.add_argument('city', action='store', nargs='?',
                        help='Find the timezone of this city')

    return parser.parse_args()


#
##############################################################################
#
# main()
#
def main():
    """
    Consider writing docstrings in the Google style:
        https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

    Where possible, add type annotations as well. For example:
        https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html

    Args:
        None
    Returns:
        Nothing
    Raises:
        Nothing
    """

    args = handle_arguments()

    # Configure logging
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s.%(funcName)s:%(message)s',
                        level=getattr(logging, args.log_level.upper()))

    logger = _get_logger()

    logger.info("Log level is '%s'", args.log_level.upper())

    local_tz = get_localzone()

    now_time = datetime.now(tz=pytz.timezone(str(local_tz)))
    utc_time = now_time.astimezone(tz=pytz.utc)

    # always show local and UTC time
    times = {
        now_time.replace(tzinfo=None): now_time,
        utc_time.replace(tzinfo=None): utc_time,
    }

    print(f"Current timezone: {now_time.tzname()}")

    tz_where = tzwhere.tzwhere()

    format_str = '%H:%M' if args.time_only else '%Y-%m-%d %H:%M'

    if args.city:

        logger.info("Reverse geocode for '%s'", args.city)

        try:
            location = geocode(args.city)

            city_tz = pytz.timezone(tz_where.tzNameAt(location.latitude, location.longitude))
            new_time = now_time.astimezone(tz=city_tz)
            print(f"{args.city.title()} timezone: " + new_time.tzname())
            times[new_time.replace(tzinfo=None)] = new_time
        except Exception as err:  # pylint: disable=broad-except
            print(err)
            logger.warning("Unable to find timezone for '%s'", args.city)

    else:
        logger.info("Resolving default cities...")
        for city_name, location in CITIES.items():
            city_tz = pytz.timezone(tz_where.tzNameAt(location[0], location[1]))
            new_time = now_time.astimezone(tz=city_tz)
            print(f"{city_name.title()} timezone: " + new_time.tzname())
            times[new_time.replace(tzinfo=None)] = new_time

    print("")
    # output report
    for the_time in sorted(times.keys(), reverse=True):
        print(f"{times[the_time].tzname()} - {times[the_time].strftime(format_str)}")


#
##############################################################################
#
# geocode
#
def geocode(city=None):
    """
    Consider writing docstrings in the Google style:
        https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

    Where possible, add type annotations as well. For example:
        https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html

    Args:
        city(str): String representation of the city name to geocode

    Returns:
        geopy.location.Location: Location object or None

    Raises:
        RuntimeError: When geocding fails
    """

    try:
        geolocator = Photon(user_agent="LazyTimezoneSearch 0.1")
        location = geolocator.geocode(city, exactly_one=True)
    except Exception as err:  # pylint: disable=broad-except
        raise RuntimeError(f"Unable to geocode: '{err}'")

    return location


#
##############################################################################
#
# Call the main function
#
if __name__ == '__main__':
    main()
