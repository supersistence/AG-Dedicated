"""Command-line interface for ag-dedicated."""

from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from ag_dedicated import config
from ag_dedicated.analysis.statute_comparison import StatuteComparison
from ag_dedicated.extractors.pdf_extractor import PDFExtractor
from ag_dedicated.scrapers.honolulu import HonoluluScraper
from ag_dedicated.scrapers.hawaii import HawaiiScraper
from ag_dedicated.scrapers.maui import MauiScraper
from ag_dedicated.scrapers.kauai import KauaiScraper
from ag_dedicated.utils.logging import setup_logging_from_config


console = Console()


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(debug: bool):
    """
    AG-Dedicated: Hawaii Agricultural Dedication Analysis Tool

    Analyze agricultural property tax dedications across all Hawaii counties.
    """
    # Setup logging
    if debug:
        config._config['logging']['level'] = 'DEBUG'

    setup_logging_from_config(config)
    config.ensure_directories()


@main.command()
@click.option(
    '--pdf-dir',
    type=click.Path(exists=True, path_type=Path),
    help='Directory containing PDF files (default from config)',
)
@click.option(
    '--output-dir',
    type=click.Path(path_type=Path),
    help='Output directory for CSVs (default from config)',
)
def extract(pdf_dir: Optional[Path], output_dir: Optional[Path]):
    """Extract dedication data from PDF reports."""
    console.print("\n[bold blue]PDF Extraction Pipeline[/bold blue]\n")

    extractor = PDFExtractor(config)

    # Run full pipeline
    df = extractor.process_all(pdf_dir=pdf_dir, output_dir=output_dir)

    if not df.empty:
        console.print(f"\n[bold green]✓ Successfully extracted {len(df):,} records[/bold green]")

        # Show summary table
        if 'Year' in df.columns:
            table = Table(title="Records by Year")
            table.add_column("Year", style="cyan")
            table.add_column("Count", style="green", justify="right")

            year_counts = df['Year'].value_counts().sort_index()
            for year, count in year_counts.items():
                table.add_row(str(year), f"{count:,}")

            console.print(table)
    else:
        console.print("[bold red]✗ Extraction failed[/bold red]")


@main.command()
@click.argument('county', type=click.Choice(['honolulu', 'hawaii', 'maui', 'kauai']))
@click.option(
    '--input-file',
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help='CSV file with dedication list (must have TMK column)',
)
@click.option(
    '--output-file',
    type=click.Path(path_type=Path),
    help='Output CSV file for scraped data',
)
@click.option(
    '--max-parcels',
    type=int,
    help='Maximum number of parcels to scrape (for testing)',
)
@click.option(
    '--tmk-column',
    default='TMK',
    help='Name of TMK column in input file',
)
def scrape(
    county: str,
    input_file: Path,
    output_file: Optional[Path],
    max_parcels: Optional[int],
    tmk_column: str,
):
    """Scrape parcel data from county databases."""
    import pandas as pd

    console.print(f"\n[bold blue]Scraping {county.title()} County Parcels[/bold blue]\n")

    # Load input file
    df = pd.read_csv(input_file)
    console.print(f"Loaded {len(df):,} records from {input_file.name}")

    if tmk_column not in df.columns:
        console.print(f"[bold red]✗ Column '{tmk_column}' not found in input file[/bold red]")
        return

    # Create appropriate scraper
    scrapers = {
        'honolulu': HonoluluScraper,
        'hawaii': HawaiiScraper,
        'maui': MauiScraper,
        'kauai': KauaiScraper,
    }

    ScraperClass = scrapers[county]

    with ScraperClass(config) as scraper:
        result_df = scraper.scrape_from_dedication_list(
            df,
            tmk_column=tmk_column,
            max_parcels=max_parcels,
        )

        if output_file:
            result_df.to_csv(output_file, index=False)
            console.print(f"\n[bold green]✓ Saved {len(result_df):,} records to {output_file}[/bold green]")


@main.command()
@click.option(
    '--output-dir',
    type=click.Path(path_type=Path),
    help='Output directory for comparison files',
)
@click.option(
    '--format',
    type=click.Choice(['text', 'csv', 'both']),
    default='both',
    help='Output format',
)
def compare(output_dir: Optional[Path], format: str):
    """Compare agricultural dedication statutes across counties."""
    console.print("\n[bold blue]County Statute Comparison[/bold blue]\n")

    comparison = StatuteComparison(config)

    if format in ['text', 'both']:
        # Generate text report
        report = comparison.generate_comparison_report()
        console.print(report)

        if output_dir:
            report_path = output_dir / 'comparison_report.txt'
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(report)
            console.print(f"\n[green]Saved report to {report_path}[/green]")

    if format in ['csv', 'both']:
        # Export CSV files
        if not output_dir:
            output_dir = config.get_path('paths.data.processed') / 'comparisons'

        comparison.export_to_csv(output_dir)
        console.print(f"\n[green]Saved CSV files to {output_dir}[/green]")


@main.command()
def info():
    """Show configuration and system information."""
    console.print("\n[bold blue]AG-Dedicated Configuration[/bold blue]\n")

    # Project info
    table = Table(title="Project Information")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Project Root", str(config.project_root))
    table.add_row("Data Directory", str(config.data_dir))
    table.add_row("Raw Data Directory", str(config.raw_data_dir))
    table.add_row("Dedication History", str(config.dedication_history_dir))

    console.print(table)

    # Counties
    counties_table = Table(title="Enabled Counties")
    counties_table.add_column("County", style="cyan")
    counties_table.add_column("Name", style="green")
    counties_table.add_column("Island", style="yellow")

    for county in config.get_enabled_counties():
        county_config = config.get_county_config(county)
        counties_table.add_row(
            county.title(),
            county_config.get('name', ''),
            county_config.get('island', ''),
        )

    console.print("\n")
    console.print(counties_table)


@main.command()
@click.argument('county', type=click.Choice(['honolulu', 'hawaii', 'maui', 'kauai', 'all']))
def county_info(county: str):
    """Show detailed information about a county's dedication program."""
    console.print(f"\n[bold blue]{county.title()} County Information[/bold blue]\n")

    comparison = StatuteComparison(config)

    counties = [county] if county != 'all' else config.get_enabled_counties()

    for c in counties:
        summary = comparison.get_county_summary(c)

        table = Table(title=summary['name'])
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        for key, value in summary.items():
            if key not in ['county', 'name']:
                table.add_row(key.replace('_', ' ').title(), str(value))

        console.print(table)
        console.print()


if __name__ == '__main__':
    main()
