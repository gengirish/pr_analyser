"""Date utility functions."""

from datetime import datetime
from dateutil import parser as date_parser
from typing import Optional, Union


def parse_date(date_str: Union[str, datetime]) -> datetime:
    """
    Parse a date string into a datetime object.
    
    Args:
        date_str: Date string or datetime object
        
    Returns:
        Parsed datetime object
    """
    if isinstance(date_str, datetime):
        return date_str
    
    return date_parser.parse(date_str)


def format_date(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object as a string.
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted date string
    """
    return dt.strftime(format_str)


def get_date_range(since: Optional[str] = None, until: Optional[str] = None) -> tuple[Optional[datetime], Optional[datetime]]:
    """
    Parse date range from strings.
    
    Args:
        since: Start date string
        until: End date string
        
    Returns:
        Tuple of (since_date, until_date)
    """
    since_date = parse_date(since) if since else None
    until_date = parse_date(until) if until else None
    
    return since_date, until_date
