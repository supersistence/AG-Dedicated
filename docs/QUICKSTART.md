# Quick Start Guide

Get up and running with AG-Dedicated v2.0 in 5 minutes.

## 1. Installation (30 seconds)

```bash
# Navigate to project directory
cd AG-Dedicated

# Install package
pip install -e .
```

## 2. Verify Installation (10 seconds)

```bash
# Check that CLI works
ag-dedicated --help

# View configuration
ag-dedicated info
```

You should see:
```
AG-Dedicated Configuration
  Project Root: /path/to/AG-Dedicated
  ...
  Enabled Counties: Honolulu, Hawaii, Maui, Kauai
```

## 3. Extract PDF Data (2 minutes)

```bash
# Extract dedication data from all PDFs
ag-dedicated extract
```

This will:
1. Extract tables from PDFs in `Dedication History/`
2. Merge all years into one file
3. Clean and validate petition numbers
4. Save to `Dedication History/output/cleaned_output.csv`

## 4. Compare Counties (10 seconds)

```bash
# Generate statute comparison report
ag-dedicated compare
```

Output shows:
- Dedication periods by county
- Assessment methods
- Application requirements
- Deadlines

## 5. Explore Analysis (2 minutes)

```bash
# Start Jupyter notebook
jupyter notebook notebooks/analysis.ipynb
```

Run all cells to see:
- Temporal trends
- Year-by-year statistics
- Geographic distribution
- County comparisons

## Common Commands

### Get County Information

```bash
# Show details for specific county
ag-dedicated county-info honolulu

# Show all counties
ag-dedicated county-info all
```

### Scrape Parcel Data (for testing)

```bash
# Scrape first 10 parcels from Honolulu
ag-dedicated scrape honolulu \
    --input-file "Dedication History/output/cleaned_output.csv" \
    --output-file "data/processed/test_scrape.csv" \
    --max-parcels 10
```

**Warning**: Web scraping is rate-limited. Start with small numbers.

### Generate Reports

```bash
# Text report
ag-dedicated compare --format text

# CSV files
ag-dedicated compare --format csv --output-dir ./reports

# Both
ag-dedicated compare --format both --output-dir ./reports
```

## Quick Python API Usage

### Extract PDFs

```python
from ag_dedicated.extractors.pdf_extractor import PDFExtractor
from ag_dedicated import config

extractor = PDFExtractor(config)
df = extractor.process_all()

print(f"Extracted {len(df):,} records")
print(df.head())
```

### Scrape One Parcel

```python
from ag_dedicated.scrapers.honolulu import HonoluluScraper
from ag_dedicated import config

with HonoluluScraper(config) as scraper:
    parcel = scraper.scrape_parcel("1-2-3-4-5")  # TMK
    print(parcel)
```

### Compare Statutes

```python
from ag_dedicated.analysis.statute_comparison import StatuteComparison
from ag_dedicated import config

comparison = StatuteComparison(config)
report = comparison.generate_comparison_report()
print(report)
```

## File Structure Quick Reference

```
Your current directory:
AG-Dedicated/
├── Dedication History/     ← PDFs go here
│   └── output/            ← Extracted CSVs here
├── data/
│   ├── processed/         ← Your analysis outputs
│   └── raw/               ← Downloaded data
├── notebooks/             ← Jupyter notebooks
├── config/config.yaml     ← Edit settings here
└── src/ag_dedicated/      ← Package code
```

## Customization

### Change Paths

Edit `config/config.yaml`:

```yaml
paths:
  dedication_history: "Dedication History"  # Your PDF folder
  output: "Dedication History/output"       # Your output folder
```

### Change Logging

Edit `config/config.yaml`:

```yaml
logging:
  level: "DEBUG"  # Change to DEBUG for verbose output
  log_to_file: true
```

### Change Rate Limiting

Edit `config/config.yaml`:

```yaml
web_scraping:
  delay_between_requests: 6  # seconds
  retry_attempts: 3
```

## Troubleshooting

### Command not found: ag-dedicated

```bash
# Reinstall package
pip install -e .

# Verify installation
which ag-dedicated
```

### No PDFs found

```bash
# Check path in config
ag-dedicated info

# Update config/config.yaml if needed
```

### Import errors

```bash
# Install all dependencies
pip install -r requirements.txt
```

## Next Steps

1. **Read Full README**: `cat README.md`
2. **Check County Programs**: `cat docs/county_programs.md`
3. **Migration Guide** (if coming from v1.0): `cat docs/MIGRATION_GUIDE.md`
4. **Explore Notebooks**: `jupyter notebook`

## Get Help

```bash
# General help
ag-dedicated --help

# Command-specific help
ag-dedicated extract --help
ag-dedicated scrape --help
ag-dedicated compare --help
```

## Example Workflow

Complete workflow from PDFs to analysis:

```bash
# 1. Extract data from PDFs
ag-dedicated extract

# 2. View what we got
ag-dedicated info

# 3. Compare county programs
ag-dedicated compare --output-dir ./reports

# 4. Test scraping (small sample)
ag-dedicated scrape honolulu \
    --input-file "Dedication History/output/cleaned_output.csv" \
    --max-parcels 5 \
    --output-file "data/processed/sample.csv"

# 5. Open Jupyter for analysis
jupyter notebook notebooks/analysis.ipynb
```

## Success Indicators

✅ CLI commands work without errors
✅ `ag-dedicated info` shows your project root
✅ `ag-dedicated extract` creates CSV files
✅ `ag-dedicated compare` generates reports
✅ Jupyter notebook runs without errors

You're ready to go! 🎉
