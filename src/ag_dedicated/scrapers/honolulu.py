"""Honolulu County (Oahu) parcel data scraper."""

from typing import Any, Dict, Optional

import pandas as pd

from ag_dedicated.scrapers.base import BaseScraper


class HonoluluScraper(BaseScraper):
    """
    Scraper for Honolulu County (Oahu) QPublic parcel database.

    Extracts ownership, assessment, land, agricultural assessment,
    and tax data for dedicated parcels.
    """

    def __init__(self, config):
        """
        Initialize Honolulu scraper.

        Args:
            config: Settings instance
        """
        super().__init__(config, 'honolulu')

        # Get QPublic URL from config
        sources = self.county_config.get('sources', {})
        self.base_url = sources.get('qpublic_url', '')

        if not self.base_url:
            raise ValueError("Honolulu QPublic URL not found in config")

    def get_parcel_url(self, tmk: str) -> str:
        """
        Get URL for parcel detail page.

        Args:
            tmk: Tax Map Key

        Returns:
            Full URL string
        """
        return f"{self.base_url}?county=hi_honolulu&KEY={tmk}"

    def get_history_url(self, tmk: str) -> str:
        """Get URL for assessment history page."""
        return f"http://qpublic9.qpublic.net/hi_honolulu_display.php?KEY={tmk}&show_history=1&"

    def get_land_print_url(self, tmk: str) -> str:
        """Get URL for land information print page."""
        return f"http://qpublic9.qpublic.net/hi_honolulu_land_print.php?KEY={tmk}"

    def scrape_parcel(self, tmk: str) -> Dict[str, Any]:
        """
        Scrape comprehensive data for a single parcel.

        This method fetches multiple pages for each parcel:
        1. Main parcel page - ownership and land info
        2. History page - assessment and tax history
        3. Land print page - detailed land info

        Args:
            tmk: Tax Map Key

        Returns:
            Dictionary with all parcel data
        """
        data = {'TMK': tmk}

        try:
            # Fetch main page
            main_url = self.get_parcel_url(tmk)
            main_response = self.fetch_url(main_url)
            main_soup = self.parse_html(main_response.text)

            # Fetch history page
            history_url = self.get_history_url(tmk)
            history_response = self.fetch_url(history_url)
            history_soup = self.parse_html(history_response.text)

            # Fetch land print page
            land_url = self.get_land_print_url(tmk)
            land_response = self.fetch_url(land_url)
            land_soup = self.parse_html(land_response.text)

            # Extract ownership information (table 3)
            ownership = self._extract_ownership(main_soup)
            data.update(ownership)

            # Extract assessment information (table 5 from history)
            assessment = self._extract_assessment(history_soup)
            data.update(assessment)

            # Extract land information (table 7)
            land_info = self._extract_land_info(main_soup)
            data.update(land_info)

            # Extract agricultural assessment (table 8)
            ag_assessment = self._extract_ag_assessment(main_soup)
            data.update(ag_assessment)

            # Extract tax information (table 15 from history)
            tax_info = self._extract_tax_info(history_soup)
            data.update(tax_info)

            self.logger.debug(f"Successfully scraped {tmk}")

        except Exception as e:
            self.logger.error(f"Error scraping {tmk}: {e}")
            data['scrape_error'] = str(e)

        return data

    def _extract_ownership(self, soup) -> Dict[str, Any]:
        """
        Extract ownership and parcel information.

        Corresponds to table 3 in original R script.
        """
        result = {}
        try:
            df = self.extract_table(soup, table_index=2, remove_first_row=True)

            if len(df) >= 2 and len(df.columns) >= 2:
                # Convert to dict - first column is label, second is value
                for _, row in df.iterrows():
                    if len(row) >= 2:
                        key = str(row.iloc[0]).strip()
                        value = str(row.iloc[1]).strip()

                        # Map to standard keys
                        if 'owner' in key.lower():
                            result['Owner'] = value
                        elif 'address' in key.lower():
                            result['Owner_Address'] = value
                        elif 'location' in key.lower() or 'property' in key.lower():
                            result['Property_Location'] = value
                        elif 'acres' in key.lower() or 'area' in key.lower():
                            result['Acres'] = value
                        elif 'zone' in key.lower():
                            result['Zone'] = value

        except Exception as e:
            self.logger.debug(f"Error extracting ownership: {e}")

        return result

    def _extract_assessment(self, history_soup) -> Dict[str, Any]:
        """
        Extract assessment history.

        Corresponds to table 5 from history page in original R script.
        Returns most recent assessment year data.
        """
        result = {}
        try:
            df = self.extract_table(
                history_soup,
                table_index=4,
                remove_first_row=True,
                remove_last_row=True
            )

            if not df.empty:
                # Get most recent year (first row after removing headers)
                recent = df.iloc[0]

                if len(recent) >= 4:
                    result['Assessment_Year'] = recent.iloc[0]
                    result['Building_Value'] = recent.iloc[1] if len(recent) > 1 else None
                    result['Land_Value'] = recent.iloc[2] if len(recent) > 2 else None
                    result['Total_Value'] = recent.iloc[3] if len(recent) > 3 else None

        except Exception as e:
            self.logger.debug(f"Error extracting assessment: {e}")

        return result

    def _extract_land_info(self, soup) -> Dict[str, Any]:
        """
        Extract land information.

        Corresponds to table 7 in original R script.
        """
        result = {}
        try:
            df = self.extract_table(soup, table_index=6)

            if not df.empty:
                # Land info typically has land use codes, classifications
                result['Land_Info_Table'] = df.to_dict('records')

        except Exception as e:
            self.logger.debug(f"Error extracting land info: {e}")

        return result

    def _extract_ag_assessment(self, soup) -> Dict[str, Any]:
        """
        Extract agricultural assessment information.

        Corresponds to table 8 in original R script.
        """
        result = {}
        try:
            df = self.extract_table(soup, table_index=7)

            if not df.empty:
                # Ag assessment details
                result['Ag_Assessment_Table'] = df.to_dict('records')

                # Try to extract key fields if present
                if len(df.columns) >= 2:
                    for _, row in df.iterrows():
                        if len(row) >= 2:
                            label = str(row.iloc[0]).lower()
                            value = str(row.iloc[1])

                            if 'dedication' in label:
                                result['Dedication_Type'] = value
                            elif 'end' in label and 'year' in label:
                                result['Dedication_End_Year'] = value

        except Exception as e:
            self.logger.debug(f"Error extracting ag assessment: {e}")

        return result

    def _extract_tax_info(self, history_soup) -> Dict[str, Any]:
        """
        Extract historical tax information.

        Corresponds to table 15 from history page in original R script.
        """
        result = {}
        try:
            df = self.extract_table(history_soup, table_index=14)

            if not df.empty:
                # Get most recent tax year
                recent = df.iloc[0]

                if len(recent) >= 2:
                    result['Tax_Year'] = recent.iloc[0]
                    result['Tax_Amount'] = recent.iloc[1] if len(recent) > 1 else None
                    result['Tax_Status'] = recent.iloc[2] if len(recent) > 2 else None

        except Exception as e:
            self.logger.debug(f"Error extracting tax info: {e}")

        return result

    def scrape_from_dedication_list(
        self,
        dedications_df: pd.DataFrame,
        tmk_column: str = 'TMK',
        max_parcels: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Scrape parcels from a dedication list DataFrame.

        Args:
            dedications_df: DataFrame with dedication data
            tmk_column: Name of TMK column
            max_parcels: Optional limit on number to scrape

        Returns:
            DataFrame with enriched parcel data
        """
        if tmk_column not in dedications_df.columns:
            raise ValueError(f"Column '{tmk_column}' not found in DataFrame")

        tmks = dedications_df[tmk_column].dropna().unique()

        if max_parcels:
            tmks = tmks[:max_parcels]

        self.logger.info(
            f"Scraping {len(tmks)} unique parcels from dedication list"
        )

        # Scrape all parcels
        scraped_df = self.scrape_parcels(tmks.tolist())

        # Merge with original dedication data
        if not scraped_df.empty:
            result = dedications_df.merge(
                scraped_df,
                left_on=tmk_column,
                right_on='TMK',
                how='left',
            )
            return result

        return dedications_df
