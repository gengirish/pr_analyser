"""Date helpers shared across analyzers."""

import datetime
import sys

from dateutil import parser as _date_parser

# The project's canonical cutoff: November 1, 2024 (UTC).
DEFAULT_TARGET_DATE = datetime.datetime(2024, 11, 1, tzinfo=datetime.timezone.utc)
DEFAULT_DATE_STR = '2024-11-01'


def parse_target_date(date_str):
    """Parse a 'YYYY-MM-DD' string into a UTC datetime.

    Prints an error and exits (matching the original scripts) when the format
    is invalid.
    """
    try:
        parsed = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return parsed.replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        print("Error: Date must be in the format YYYY-MM-DD")
        sys.exit(1)


def parse_timestamp(value):
    """Parse an ISO-8601 timestamp (e.g. a PR's merged_at) into a datetime."""
    return _date_parser.parse(value)
