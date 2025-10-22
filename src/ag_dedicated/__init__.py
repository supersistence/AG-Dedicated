"""
AG-Dedicated: Analysis of Hawaii's Agricultural Property Tax Dedication System

This package provides tools for:
- Extracting agricultural dedication data from PDFs across all Hawaii counties
- Scraping public parcel and tax data from county databases
- Analyzing dedication patterns and tax benefits
- Comparing agricultural dedication statutes across counties
"""

__version__ = "2.0.0"
__author__ = "AG-Dedicated Project"

from ag_dedicated.config.settings import Settings

# Singleton config instance
config = Settings()

__all__ = ["config", "Settings"]
