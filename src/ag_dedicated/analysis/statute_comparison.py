"""Statute and policy comparison across Hawaii counties."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from loguru import logger

from ag_dedicated.config.settings import Settings


class StatuteComparison:
    """
    Compare agricultural dedication statutes and policies across counties.

    Analyzes differences in:
    - Dedication periods
    - Assessment rates
    - Minimum requirements
    - Application deadlines
    - Compliance rules
    """

    def __init__(self, config: Optional[Settings] = None):
        """
        Initialize statute comparison.

        Args:
            config: Settings instance
        """
        self.config = config or Settings()
        self.logger = logger.bind(name=__name__)

    def get_county_summary(self, county: str) -> Dict[str, Any]:
        """
        Get summary of dedication program for a county.

        Args:
            county: County name

        Returns:
            Dictionary with program details
        """
        county_config = self.config.get_county_config(county)

        summary = {
            'county': county.title(),
            'name': county_config.get('name'),
            'island': county_config.get('island'),
            'enabled': county_config.get('enabled'),
            'dedication_periods': county_config.get('dedication_periods', []),
            'application_deadline': county_config.get('application_deadline'),
        }

        # Add county-specific details
        if county == 'honolulu':
            summary['assessment_rates'] = county_config.get('assessment_rates', {})
            summary['min_agricultural_use'] = county_config.get('min_agricultural_use')

        elif county == 'hawaii':
            summary['programs'] = county_config.get('programs', [])
            summary['min_gross_income'] = county_config.get('min_gross_income')

        elif county == 'maui':
            summary['tax_rate'] = county_config.get('tax_rate')
            summary['note'] = county_config.get('note')

        elif county == 'kauai':
            summary['office'] = county_config.get('office', {})
            summary['recent_changes'] = county_config.get('recent_changes')

        return summary

    def compare_all_counties(self) -> pd.DataFrame:
        """
        Create comparison table of all counties.

        Returns:
            DataFrame with county comparisons
        """
        counties = self.config.get_enabled_counties()

        comparisons = []
        for county in counties:
            summary = self.get_county_summary(county)
            comparisons.append(summary)

        df = pd.DataFrame(comparisons)

        self.logger.info(f"Compared {len(comparisons)} counties")

        return df

    def compare_dedication_periods(self) -> pd.DataFrame:
        """
        Compare dedication period options across counties.

        Returns:
            DataFrame showing which periods each county offers
        """
        counties = self.config.get_enabled_counties()

        # Collect all unique periods
        all_periods = set()
        county_periods = {}

        for county in counties:
            config = self.config.get_county_config(county)
            periods = config.get('dedication_periods', [])
            county_periods[county] = periods
            all_periods.update(periods)

        # Create comparison matrix
        periods_sorted = sorted(all_periods)
        data = []

        for county in counties:
            row = {'County': county.title()}
            for period in periods_sorted:
                row[f'{period}_year'] = period in county_periods[county]
            data.append(row)

        df = pd.DataFrame(data)

        return df

    def compare_requirements(self) -> List[Dict[str, Any]]:
        """
        Compare eligibility requirements across counties.

        Returns:
            List of requirement comparisons
        """
        counties = self.config.get_enabled_counties()

        requirements = []

        for county in counties:
            config = self.config.get_county_config(county)

            req = {
                'county': county.title(),
                'deadline': config.get('application_deadline', 'Not specified'),
            }

            # County-specific requirements
            if county == 'honolulu':
                req['min_ag_use'] = f"{config.get('min_agricultural_use', 0)*100}% of usable land"
                req['income_requirement'] = 'Revenue-generating production'

            elif county == 'hawaii':
                req['min_gross_income'] = f"${config.get('min_gross_income', 0):,}/year"
                req['proof_required'] = 'Yes - agricultural production'

            elif county == 'maui':
                req['assessment_discount'] = 'Greater discounts for longer periods'

            elif county == 'kauai':
                req['recent_changes'] = config.get('recent_changes', 'None')

            requirements.append(req)

        return requirements

    def generate_comparison_report(
        self,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate comprehensive comparison report.

        Args:
            output_path: Optional path to save report

        Returns:
            Report text
        """
        report_lines = []

        report_lines.append("=" * 80)
        report_lines.append("HAWAII AGRICULTURAL DEDICATION PROGRAM COMPARISON")
        report_lines.append("=" * 80)
        report_lines.append("")

        # Overall summary
        counties = self.config.get_enabled_counties()
        report_lines.append(f"Comparing {len(counties)} counties: {', '.join(c.title() for c in counties)}")
        report_lines.append("")

        # Dedication periods comparison
        report_lines.append("-" * 80)
        report_lines.append("DEDICATION PERIODS BY COUNTY")
        report_lines.append("-" * 80)

        for county in counties:
            config = self.config.get_county_config(county)
            periods = config.get('dedication_periods', [])
            periods_str = ', '.join(f"{p} year" for p in sorted(periods))
            report_lines.append(f"{config['name']}: {periods_str}")

        report_lines.append("")

        # Requirements comparison
        report_lines.append("-" * 80)
        report_lines.append("REQUIREMENTS BY COUNTY")
        report_lines.append("-" * 80)

        requirements = self.compare_requirements()
        for req in requirements:
            report_lines.append(f"\n{req['county']}:")
            for key, value in req.items():
                if key != 'county':
                    report_lines.append(f"  {key.replace('_', ' ').title()}: {value}")

        report_lines.append("")

        # Assessment methods
        report_lines.append("-" * 80)
        report_lines.append("ASSESSMENT METHODS")
        report_lines.append("-" * 80)

        for county in counties:
            config = self.config.get_county_config(county)
            report_lines.append(f"\n{config['name']}:")

            if county == 'honolulu':
                rates = config.get('assessment_rates', {})
                report_lines.append(f"  5-year: {rates.get('5_year', 0)*100}% of fair market value")
                report_lines.append(f"  10-year: {rates.get('10_year', 0)*100}% of fair market value")

            elif county == 'hawaii':
                programs = config.get('programs', [])
                for prog in programs:
                    report_lines.append(f"  {prog['name']}: {prog.get('note', '')}")

            elif county == 'maui':
                tax_rate = config.get('tax_rate', 0)
                report_lines.append(f"  Tax rate: ${tax_rate}/\u0243000 assessed value")
                report_lines.append(f"  Note: {config.get('note', '')}")

            elif county == 'kauai':
                report_lines.append("  5-year commitment to commercial farming")
                report_lines.append("  Reduced property tax rate")

        report_lines.append("")
        report_lines.append("=" * 80)

        report = "\n".join(report_lines)

        # Save to file if requested
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(report)
            self.logger.info(f"Saved comparison report to {output_path}")

        return report

    def export_to_csv(self, output_dir: Path) -> None:
        """
        Export comparison data to CSV files.

        Args:
            output_dir: Directory for output files
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # County summary
        summary_df = self.compare_all_counties()
        summary_df.to_csv(output_dir / 'county_summary.csv', index=False)

        # Dedication periods
        periods_df = self.compare_dedication_periods()
        periods_df.to_csv(output_dir / 'dedication_periods.csv', index=False)

        # Requirements
        requirements = self.compare_requirements()
        req_df = pd.DataFrame(requirements)
        req_df.to_csv(output_dir / 'requirements.csv', index=False)

        self.logger.info(f"Exported comparison data to {output_dir}")
