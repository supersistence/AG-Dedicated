"""PDF extraction utilities for agricultural dedication reports."""

import re
from pathlib import Path
from typing import Optional

import pandas as pd
import tabula
from loguru import logger

from ag_dedicated.config.settings import Settings
from ag_dedicated.utils.validation import validate_petition_number, clean_petition_number


class PDFExtractor:
    """
    Extract tabular data from agricultural dedication PDF reports.

    Handles extraction, cleaning, and merging of dedication data across
    multiple years and counties.
    """

    def __init__(self, config: Optional[Settings] = None):
        """
        Initialize PDF extractor.

        Args:
            config: Settings instance (creates new one if not provided)
        """
        self.config = config or Settings()
        self.logger = logger.bind(name=__name__)

    def extract_pdf(
        self,
        pdf_path: Path,
        output_path: Optional[Path] = None,
        pages: str = 'all',
    ) -> Optional[pd.DataFrame]:
        """
        Extract tables from a single PDF file.

        Args:
            pdf_path: Path to PDF file
            output_path: Optional path to save CSV output
            pages: Pages to extract ('all' or specific pages like '1-3')

        Returns:
            DataFrame with extracted data, or None if extraction failed
        """
        if not pdf_path.exists():
            self.logger.error(f"PDF file not found: {pdf_path}")
            return None

        self.logger.info(f"Extracting tables from {pdf_path.name}")

        try:
            # Use tabula to extract tables
            dfs = tabula.read_pdf(
                str(pdf_path),
                pages=pages,
                multiple_tables=True,
                pandas_options={'header': 0}
            )

            if not dfs:
                self.logger.warning(f"No tables found in {pdf_path.name}")
                return None

            # Combine all tables from all pages
            combined_df = pd.concat(dfs, ignore_index=True)

            self.logger.info(
                f"Extracted {len(combined_df)} rows from {len(dfs)} tables "
                f"in {pdf_path.name}"
            )

            # Save to CSV if output path provided
            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                combined_df.to_csv(output_path, index=False)
                self.logger.debug(f"Saved to {output_path}")

            return combined_df

        except Exception as e:
            self.logger.error(f"Error extracting {pdf_path.name}: {e}")
            return None

    def extract_directory(
        self,
        pdf_dir: Path,
        output_dir: Path,
        pattern: str = "*.pdf",
    ) -> dict[str, pd.DataFrame]:
        """
        Extract tables from all PDFs in a directory.

        Args:
            pdf_dir: Directory containing PDF files
            output_dir: Directory for CSV output files
            pattern: Glob pattern for PDF files

        Returns:
            Dictionary mapping filename to DataFrame
        """
        if not pdf_dir.exists():
            self.logger.error(f"PDF directory not found: {pdf_dir}")
            return {}

        output_dir.mkdir(parents=True, exist_ok=True)

        pdf_files = sorted(pdf_dir.glob(pattern))
        if not pdf_files:
            self.logger.warning(f"No PDF files found matching {pattern} in {pdf_dir}")
            return {}

        self.logger.info(f"Found {len(pdf_files)} PDF files to process")

        results = {}
        for pdf_path in pdf_files:
            # Skip files in subdirectories if we only want top-level
            if pdf_path.parent != pdf_dir:
                continue

            output_path = output_dir / f"{pdf_path.stem}.csv"
            df = self.extract_pdf(pdf_path, output_path)

            if df is not None:
                results[pdf_path.name] = df

        self.logger.info(f"Successfully extracted {len(results)} PDF files")
        return results

    def extract_year_from_filename(self, filename: str) -> Optional[str]:
        """
        Extract 4-digit year from filename.

        Args:
            filename: PDF or CSV filename

        Returns:
            Year as string, or None if not found

        Examples:
            >>> extractor = PDFExtractor()
            >>> extractor.extract_year_from_filename("ag_1yr 2015.pdf")
            '2015'
            >>> extractor.extract_year_from_filename("2020_dedications.pdf")
            '2020'
        """
        year_pattern = re.compile(r'(19|20)\d{2}')
        match = year_pattern.search(filename)
        return match.group(0) if match else None

    def merge_csv_files(
        self,
        csv_dir: Path,
        output_path: Path,
        pattern: str = "*.csv",
    ) -> pd.DataFrame:
        """
        Merge multiple CSV files with year labeling.

        Args:
            csv_dir: Directory containing CSV files
            output_path: Path for merged output CSV
            pattern: Glob pattern for CSV files

        Returns:
            Merged DataFrame with 'Year' column added
        """
        csv_files = sorted(csv_dir.glob(pattern))

        if not csv_files:
            self.logger.warning(f"No CSV files found in {csv_dir}")
            return pd.DataFrame()

        self.logger.info(f"Merging {len(csv_files)} CSV files")

        dfs = []
        for csv_path in csv_files:
            try:
                df = pd.read_csv(csv_path)

                if df.empty:
                    self.logger.debug(f"Skipping empty file: {csv_path.name}")
                    continue

                # Extract and add year
                year = self.extract_year_from_filename(csv_path.name)
                if year:
                    df['Year'] = year
                    self.logger.debug(f"{csv_path.name} -> Year {year} ({len(df)} rows)")
                else:
                    df['Year'] = 'Unknown'
                    self.logger.warning(f"Could not extract year from {csv_path.name}")

                dfs.append(df)

            except Exception as e:
                self.logger.error(f"Error reading {csv_path.name}: {e}")
                continue

        if not dfs:
            self.logger.error("No valid CSV files were processed")
            return pd.DataFrame()

        # Merge all dataframes
        merged_df = pd.concat(dfs, ignore_index=True)

        # Save merged file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        merged_df.to_csv(output_path, index=False)

        self.logger.info(
            f"Merged {len(dfs)} files into {len(merged_df)} total rows "
            f"-> {output_path.name}"
        )

        # Show year distribution
        if 'Year' in merged_df.columns:
            year_counts = merged_df['Year'].value_counts().sort_index()
            self.logger.info(f"Row counts by year:\n{year_counts}")

        return merged_df

    def clean_petition_numbers(
        self,
        df: pd.DataFrame,
        petition_col: str = 'Petition Number',
        numeric_only: bool = True,
    ) -> pd.DataFrame:
        """
        Clean DataFrame to keep only valid petition numbers.

        Args:
            df: DataFrame to clean
            petition_col: Name of petition number column
            numeric_only: If True, keep only numeric petition numbers

        Returns:
            Cleaned DataFrame
        """
        if petition_col not in df.columns:
            self.logger.error(f"Column '{petition_col}' not found in DataFrame")
            available = ', '.join(df.columns[:10])
            self.logger.error(f"Available columns: {available}...")
            return df

        original_count = len(df)

        # Clean the petition numbers
        df[petition_col] = df[petition_col].apply(clean_petition_number)

        # Filter based on validation
        if numeric_only:
            df = df[df[petition_col].apply(
                lambda x: validate_petition_number(x, numeric_only=True)
            )]
        else:
            df = df[df[petition_col].notna()]

        cleaned_count = len(df)
        removed_count = original_count - cleaned_count

        self.logger.info(
            f"Cleaned petition numbers: kept {cleaned_count:,} rows, "
            f"removed {removed_count:,} rows ({removed_count/original_count*100:.1f}%)"
        )

        return df

    def process_all(
        self,
        pdf_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None,
    ) -> pd.DataFrame:
        """
        Complete pipeline: extract PDFs, merge CSVs, and clean data.

        Args:
            pdf_dir: Directory with PDF files (uses config if not provided)
            output_dir: Output directory (uses config if not provided)

        Returns:
            Final cleaned DataFrame
        """
        # Use config defaults if not provided
        if pdf_dir is None:
            pdf_dir = self.config.dedication_history_dir

        if output_dir is None:
            output_dir = self.config.get_path('paths.output')

        self.logger.info("=" * 60)
        self.logger.info("Starting full PDF extraction pipeline")
        self.logger.info("=" * 60)

        # Step 1: Extract PDFs to CSVs
        self.logger.info("\n[Step 1/3] Extracting PDF files...")
        extracted = self.extract_directory(pdf_dir, output_dir)

        if not extracted:
            self.logger.error("No PDFs were successfully extracted. Aborting.")
            return pd.DataFrame()

        # Step 2: Merge all CSVs
        self.logger.info("\n[Step 2/3] Merging CSV files...")
        merged_path = output_dir / 'merged_output.csv'
        merged_df = self.merge_csv_files(output_dir, merged_path)

        if merged_df.empty:
            self.logger.error("Merge resulted in empty DataFrame. Aborting.")
            return pd.DataFrame()

        # Step 3: Clean petition numbers
        self.logger.info("\n[Step 3/3] Cleaning petition numbers...")
        cleaned_df = self.clean_petition_numbers(merged_df)

        cleaned_path = output_dir / 'cleaned_output.csv'
        cleaned_df.to_csv(cleaned_path, index=False)
        self.logger.info(f"Saved cleaned data to {cleaned_path}")

        self.logger.info("=" * 60)
        self.logger.info(f"Pipeline complete! Final dataset: {len(cleaned_df):,} rows")
        self.logger.info("=" * 60)

        return cleaned_df
