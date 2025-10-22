"""Base scraper class for county parcel data."""

import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential


class BaseScraper(ABC):
    """
    Abstract base class for county parcel data scrapers.

    Provides common functionality for web scraping with rate limiting,
    error handling, and retry logic.
    """

    def __init__(self, config, county_name: str):
        """
        Initialize scraper.

        Args:
            config: Settings instance
            county_name: Name of county (honolulu, hawaii, maui, kauai)
        """
        self.config = config
        self.county_name = county_name.lower()
        self.county_config = config.get_county_config(self.county_name)
        self.logger = logger.bind(name=f"{__name__}.{county_name}")

        # Web scraping settings
        web_config = config.get('web_scraping', {})
        self.user_agent = web_config.get('user_agent', 'Mozilla/5.0')
        self.timeout = web_config.get('timeout', 30)
        self.retry_attempts = web_config.get('retry_attempts', 3)
        self.delay = web_config.get('rate_limit', {}).get('delay_between_requests', 3)

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})

        self._request_count = 0
        self._last_request_time = 0

    def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time

        if time_since_last < self.delay:
            sleep_time = self.delay - time_since_last
            self.logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)

        self._last_request_time = time.time()
        self._request_count += 1

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def fetch_url(self, url: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Fetch URL with retry logic and rate limiting.

        Args:
            url: URL to fetch
            params: Optional query parameters

        Returns:
            Response object

        Raises:
            requests.RequestException on failure after retries
        """
        self._rate_limit()

        self.logger.debug(f"Fetching: {url}")
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()

        return response

    def parse_html(self, html_content: str) -> BeautifulSoup:
        """
        Parse HTML content.

        Args:
            html_content: HTML string

        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html_content, 'lxml')

    def extract_table(
        self,
        soup: BeautifulSoup,
        table_index: int,
        remove_first_row: bool = False,
        remove_last_row: bool = False,
    ) -> pd.DataFrame:
        """
        Extract table from HTML.

        Args:
            soup: BeautifulSoup object
            table_index: Index of table to extract (0-based)
            remove_first_row: Remove first row (redundant header)
            remove_last_row: Remove last row (footer note)

        Returns:
            DataFrame with table data
        """
        tables = soup.find_all('table')

        if table_index >= len(tables):
            self.logger.warning(
                f"Table index {table_index} out of range "
                f"(found {len(tables)} tables)"
            )
            return pd.DataFrame()

        # Convert HTML table to DataFrame
        df = pd.read_html(str(tables[table_index]))[0]

        # Remove rows if requested
        if remove_first_row and len(df) > 0:
            df = df.iloc[1:]

        if remove_last_row and len(df) > 0:
            df = df.iloc[:-1]

        return df.reset_index(drop=True)

    @abstractmethod
    def scrape_parcel(self, identifier: str) -> Dict[str, Any]:
        """
        Scrape data for a single parcel.

        Args:
            identifier: Parcel identifier (TMK, etc.)

        Returns:
            Dictionary with parcel data
        """
        pass

    @abstractmethod
    def get_parcel_url(self, identifier: str) -> str:
        """
        Get URL for parcel detail page.

        Args:
            identifier: Parcel identifier

        Returns:
            Full URL string
        """
        pass

    def scrape_parcels(
        self,
        identifiers: list[str],
        save_path: Optional[Path] = None,
    ) -> pd.DataFrame:
        """
        Scrape data for multiple parcels.

        Args:
            identifiers: List of parcel identifiers
            save_path: Optional path to save results

        Returns:
            DataFrame with all parcel data
        """
        self.logger.info(f"Scraping {len(identifiers)} parcels for {self.county_name}")

        results = []
        for i, identifier in enumerate(identifiers, 1):
            try:
                self.logger.debug(f"[{i}/{len(identifiers)}] Scraping {identifier}")
                data = self.scrape_parcel(identifier)
                if data:
                    results.append(data)

            except Exception as e:
                self.logger.error(f"Error scraping {identifier}: {e}")
                continue

            # Progress update every 10 parcels
            if i % 10 == 0:
                self.logger.info(f"Progress: {i}/{len(identifiers)} parcels processed")

        df = pd.DataFrame(results)

        if save_path and not df.empty:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(save_path, index=False)
            self.logger.info(f"Saved {len(df)} records to {save_path}")

        self.logger.info(
            f"Scraping complete: {len(results)} successful out of {len(identifiers)}"
        )

        return df

    def close(self):
        """Close session and cleanup resources."""
        self.session.close()
        self.logger.debug("Scraper session closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
