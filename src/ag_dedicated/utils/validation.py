"""Data validation utilities."""

import re
from typing import Any, Optional


def validate_petition_number(value: Any, numeric_only: bool = True) -> bool:
    """
    Validate petition number format.

    Args:
        value: Value to validate
        numeric_only: If True, only accept numeric petition numbers

    Returns:
        True if valid, False otherwise

    Examples:
        >>> validate_petition_number("12345")
        True
        >>> validate_petition_number("AG-12345")
        False
        >>> validate_petition_number("AG-12345", numeric_only=False)
        True
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False

    value_str = str(value).strip()

    if not value_str:
        return False

    if numeric_only:
        return value_str.isdigit()
    else:
        # Accept alphanumeric with optional dashes/underscores
        return bool(re.match(r'^[A-Z0-9-_]+$', value_str, re.IGNORECASE))


def validate_tmk(tmk: str) -> bool:
    """
    Validate Hawaii Tax Map Key (TMK) format.

    TMK format variations:
    - 1-2-3-4-5 (zone-section-plat-parcel-cpt)
    - 12345 (condensed)
    - 1-2-3-4 (4 components)

    Args:
        tmk: TMK string to validate

    Returns:
        True if valid TMK format, False otherwise

    Examples:
        >>> validate_tmk("1-2-3-4-5")
        True
        >>> validate_tmk("12345")
        True
        >>> validate_tmk("invalid")
        False
    """
    if not tmk or not isinstance(tmk, str):
        return False

    tmk = tmk.strip()

    # Pattern 1: Dash-separated (4 or 5 components)
    dash_pattern = r'^\d+-\d+-\d+-\d+(?:-\d+)?$'
    if re.match(dash_pattern, tmk):
        return True

    # Pattern 2: Condensed numeric (at least 4 digits)
    if re.match(r'^\d{4,}$', tmk):
        return True

    return False


def validate_year(year: Any, min_year: int = 2000, max_year: Optional[int] = None) -> bool:
    """
    Validate year value.

    Args:
        year: Year value to validate
        min_year: Minimum valid year
        max_year: Maximum valid year (defaults to current year + 1)

    Returns:
        True if valid year, False otherwise
    """
    if max_year is None:
        from datetime import datetime
        max_year = datetime.now().year + 1

    try:
        year_int = int(year)
        return min_year <= year_int <= max_year
    except (ValueError, TypeError):
        return False


def validate_dataframe_columns(df, required_columns: list[str]) -> tuple[bool, list[str]]:
    """
    Validate that DataFrame has required columns.

    Args:
        df: pandas DataFrame to validate
        required_columns: List of required column names

    Returns:
        Tuple of (is_valid, missing_columns)
    """
    missing = [col for col in required_columns if col not in df.columns]
    return len(missing) == 0, missing


def clean_petition_number(value: Any) -> Optional[str]:
    """
    Clean and standardize petition number.

    Args:
        value: Raw petition number value

    Returns:
        Cleaned petition number string or None if invalid
    """
    if value is None:
        return None

    value_str = str(value).strip()

    if not value_str or value_str.lower() in ['nan', 'none', 'null', '']:
        return None

    # Remove common prefixes
    value_str = re.sub(r'^(AG|PETITION|PET)[-_\s]*', '', value_str, flags=re.IGNORECASE)

    # Keep only alphanumeric and dashes
    value_str = re.sub(r'[^A-Z0-9-]', '', value_str, flags=re.IGNORECASE)

    return value_str if value_str else None


def clean_tmk(tmk: Any) -> Optional[str]:
    """
    Clean and standardize TMK format.

    Args:
        tmk: Raw TMK value

    Returns:
        Cleaned TMK string or None if invalid
    """
    if tmk is None:
        return None

    tmk_str = str(tmk).strip()

    if not tmk_str or tmk_str.lower() in ['nan', 'none', 'null', '']:
        return None

    # Remove spaces and ensure consistent dash format
    tmk_str = tmk_str.replace(' ', '')

    if validate_tmk(tmk_str):
        return tmk_str

    return None


# Import pandas here to avoid circular imports
try:
    import pandas as pd
except ImportError:
    pd = None
