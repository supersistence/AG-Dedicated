# Migration Guide: v1.0 (R) → v2.0 (Python)

## Overview

AG-Dedicated v2.0 is a complete rewrite in Python with expanded capabilities. This guide helps you transition from the old R-based workflow to the new Python-based system.

## What Changed

### Language & Architecture
- **Before**: R + Python hybrid (R Markdown, rvest for scraping, Python for PDFs)
- **After**: Pure Python with modern package structure

### Key Improvements

| Feature | v1.0 (R) | v2.0 (Python) |
|---------|----------|---------------|
| **Counties** | Honolulu only | All 4 Hawaii counties |
| **CLI** | Manual script execution | Unified `ag-dedicated` command |
| **Paths** | Hardcoded absolute paths | Configurable, relative paths |
| **Error Handling** | Basic try/catch | Comprehensive logging & retries |
| **Data Validation** | Manual checks | Built-in validation framework |
| **Configuration** | Scattered in code | Centralized YAML config |
| **Documentation** | R Markdown only | Jupyter notebooks + docs |
| **Installation** | Manual dependencies | Standard pip install |

## File Mapping

### Scripts

| Old (v1.0) | New (v2.0) | Notes |
|------------|------------|-------|
| `RPAD_Scraper.R` | `src/ag_dedicated/scrapers/honolulu.py` | Converted to Python, added error handling |
| `pdf-scrape.py` | `src/ag_dedicated/extractors/pdf_extractor.py` | Refactored with classes, fixed paths |
| `merge clean.py` | Built into `PDFExtractor.clean_petition_numbers()` | Now part of extraction pipeline |
| `wrangle.py` | Example in `notebooks/analysis.ipynb` | Replaced with comprehensive notebook |
| `AG-Dedication.Rmd` | `notebooks/analysis.ipynb` | Converted to Jupyter notebook |

### Data

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `Dedication History/*.pdf` | Same | No change |
| `Dedication History/output/*.csv` | Same | Still used for output |
| N/A | `data/raw/` | New: for downloaded data |
| N/A | `data/processed/` | New: for cleaned datasets |
| N/A | `data/statutes/` | New: for legal documents |

## Installation

### Old Way (v1.0)

```r
# Install R packages manually
install.packages("rvest")
install.packages("tabulizer")
install.packages("dplyr")

# Install Python packages manually
pip install tabula-py pandas matplotlib
```

### New Way (v2.0)

```bash
# One command to install everything
pip install -e .

# Or just dependencies
pip install -r requirements.txt
```

## Usage Examples

### PDF Extraction

#### Old Way (v1.0)

```r
# Edit script paths manually
# Run entire R Markdown document
# Or run individual code chunks
library(tabulizer)
table <- extract_tables("~/Documents/GitHub/AG-Dedicated/Dedication History/2015_ag_1yr.pdf")
# ... manual processing ...
```

#### New Way (v2.0)

```bash
# Command line
ag-dedicated extract

# Or in Python
from ag_dedicated.extractors.pdf_extractor import PDFExtractor
extractor = PDFExtractor()
df = extractor.process_all()
```

### Web Scraping

#### Old Way (v1.0)

```r
# Edit RPAD_Scraper.R
# Update TMK manually
dedications$TMK[2]  # Access specific TMK

# Run script
source("RPAD_Scraper.R")
```

#### New Way (v2.0)

```bash
# Command line
ag-dedicated scrape honolulu \
    --input-file "Dedication History/output/cleaned_output.csv" \
    --output-file "data/processed/enriched.csv"

# Or in Python
from ag_dedicated.scrapers.honolulu import HonoluluScraper
from ag_dedicated import config

with HonoluluScraper(config) as scraper:
    data = scraper.scrape_parcel("1-2-3-4-5")
```

### Analysis

#### Old Way (v1.0)

```r
# Open AG-Dedication.Rmd in RStudio
# Run chunks manually
# Knit to HTML
```

#### New Way (v2.0)

```bash
# Start Jupyter
jupyter notebook notebooks/analysis.ipynb

# Or use the comparison tool
ag-dedicated compare --format both --output-dir ./reports
```

## Configuration Migration

### Old Way: Hardcoded Paths

```python
# In pdf-scrape.py
pdf_dir = '/Users/hh/Library/Mobile Documents/com~apple~CloudDocs/...'
```

### New Way: Config File

```yaml
# config/config.yaml
paths:
  dedication_history: "Dedication History"
  output: "Dedication History/output"
```

### Updating Paths

1. Open `config/config.yaml`
2. Update paths if your directory structure differs
3. Use relative paths from project root

## Data Migration

### No Migration Needed!

Your existing data works as-is:

```bash
# Existing PDFs
Dedication History/*.pdf  ✓ Works

# Existing CSV outputs
Dedication History/output/*.csv  ✓ Works
```

### Optional: Reorganize Data

```bash
# Move processed data to new structure
mv "Dedication History/output/cleaned_output.csv" data/processed/

# Update config to point to new location
# Or use --input-file flag in CLI
```

## Common Tasks

### Task 1: Extract All PDFs

**Old:**
```python
python pdf-scrape.py  # Edit paths first!
```

**New:**
```bash
ag-dedicated extract
```

### Task 2: Scrape 10 Parcels for Testing

**Old:**
```r
# Edit RPAD_Scraper.R
# Change loop to iterate over first 10 TMKs
for(i in dedications$TMK[1:10]) { ... }
```

**New:**
```bash
ag-dedicated scrape honolulu \
    --input-file "Dedication History/output/cleaned_output.csv" \
    --max-parcels 10
```

### Task 3: Compare County Programs

**Old:**
Not available in v1.0

**New:**
```bash
ag-dedicated compare
```

### Task 4: Check Configuration

**Old:**
Read through code files

**New:**
```bash
ag-dedicated info
ag-dedicated county-info all
```

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
pip install -e .
# Or
pip install -r requirements.txt
```

### Issue: "FileNotFoundError: config.yaml"

**Solution:**
Make sure you're running commands from project root:
```bash
cd /path/to/AG-Dedicated
ag-dedicated info
```

### Issue: "No PDF files found"

**Solution:**
Check config.yaml paths:
```yaml
paths:
  dedication_history: "Dedication History"  # Relative to project root
```

### Issue: Old scripts not working

**Solution:**
Old scripts still work but are deprecated. Use new CLI:

```bash
# Instead of:
python pdf-scrape.py

# Use:
ag-dedicated extract
```

## Feature Parity Checklist

✅ **Fully Migrated:**
- [x] PDF extraction (tabula)
- [x] CSV merging by year
- [x] Petition number cleaning
- [x] Honolulu QPublic scraping
- [x] Ownership data extraction
- [x] Assessment history
- [x] Tax information
- [x] Data visualization

🔨 **Enhanced:**
- [x] Configuration management
- [x] Error handling & retries
- [x] Logging
- [x] Data validation
- [x] CLI interface

✨ **New Features:**
- [x] Multi-county support
- [x] Statute comparison
- [x] County-specific scrapers
- [x] Modern packaging
- [x] Comprehensive documentation

## Next Steps

1. **Install v2.0**: `pip install -e .`
2. **Test extraction**: `ag-dedicated extract`
3. **Compare counties**: `ag-dedicated compare`
4. **Explore notebook**: `jupyter notebook notebooks/analysis.ipynb`
5. **Read docs**: Check `docs/` folder

## Getting Help

- **Documentation**: See `README.md` and `docs/`
- **Examples**: Check `notebooks/analysis.ipynb`
- **CLI help**: `ag-dedicated --help`
- **Command help**: `ag-dedicated <command> --help`

## Keeping Legacy Files

The old R and Python files are preserved:

```
AG-Dedicated/
├── RPAD_Scraper.R          # Legacy (still works)
├── pdf-scrape.py           # Legacy (still works)
├── wrangle.py              # Legacy
├── AG-Dedication.Rmd       # Legacy
└── merge clean.py          # Legacy
```

You can delete these after confirming v2.0 works for your needs.

## Benefits of Migration

1. **No Path Editing**: Configuration file handles all paths
2. **Better Errors**: Clear error messages and logging
3. **Multi-County**: Expand beyond Honolulu
4. **Reproducible**: Anyone can run with `pip install -e .`
5. **Professional**: Standard Python package structure
6. **Maintainable**: Organized code, tests, documentation
7. **Extensible**: Easy to add new counties/features

## Rollback Plan

If you need to revert to v1.0:

1. Keep old files (they're not deleted)
2. Use git to restore: `git checkout <old-commit>`
3. Reinstall R packages if needed
4. Continue using old workflow

However, we recommend spending a few minutes with v2.0 - it's worth it!
