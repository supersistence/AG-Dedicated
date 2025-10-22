![cover](/@yamauchi_1980%20cover.png)

# AG-Dedicated v2.0

**Comprehensive analysis of Hawaii's agricultural property tax dedication system across all counties.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

AG-Dedicated is a modernized data science toolkit for analyzing agricultural land dedication programs across Hawaii's four counties. The project extracts, processes, and analyzes dedication data to understand tax incentive programs, compliance patterns, and policy differences across jurisdictions.

### What are Agricultural Dedications?

Agricultural dedications (also called differential assessments) allow farmland to be taxed based on its agricultural use value rather than fair market value. Established in Hawaii in 1963, these programs provide significant property tax relief to encourage agricultural production and farmland preservation.

**Key Benefits:**
- Reduced property tax burden for farmers
- Preservation of agricultural land
- Support for local food production
- Multi-generational farm sustainability

## Features

✨ **Multi-County Support**: Analyze all four Hawaii counties (Honolulu, Hawaii, Maui, Kauai)

📊 **PDF Extraction**: Automated extraction of dedication data from annual RPAD reports

🌐 **Web Scraping**: Collect parcel and tax data from county QPublic databases

📈 **Comparative Analysis**: Compare statute requirements and benefits across counties

🔍 **Data Validation**: Built-in validation for TMK, petition numbers, and data quality

💻 **Modern CLI**: Rich command-line interface for all operations

📓 **Jupyter Integration**: Interactive notebooks for analysis and visualization

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AG-Dedicated.git
cd AG-Dedicated

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in development mode
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

### Basic Usage

```bash
# Show configuration and county information
ag-dedicated info

# Extract dedication data from PDFs
ag-dedicated extract

# Compare county statutes
ag-dedicated compare --format both --output-dir ./output

# Get county-specific information
ag-dedicated county-info honolulu

# Scrape parcel data (Honolulu example)
ag-dedicated scrape honolulu \
    --input-file "Dedication History/output/cleaned_output.csv" \
    --output-file "./data/processed/honolulu_enriched.csv" \
    --max-parcels 10  # For testing
```

## Project Structure

```
AG-Dedicated/
├── src/ag_dedicated/           # Main package
│   ├── config/                 # Configuration management
│   ├── extractors/             # PDF extraction tools
│   ├── scrapers/               # Web scrapers per county
│   ├── analysis/               # Analysis and comparison tools
│   ├── utils/                  # Utilities (logging, validation)
│   └── cli.py                  # Command-line interface
├── notebooks/                  # Jupyter analysis notebooks
├── data/
│   ├── raw/                    # Raw downloaded data
│   ├── processed/              # Cleaned and processed data
│   └── statutes/               # Legal documents and ordinances
├── Dedication History/         # Historical PDF reports (2013-2024)
│   └── output/                 # Extracted CSV files
├── config/                     # Configuration files
│   └── config.yaml            # Main configuration
├── docs/                       # Documentation
│   └── county_programs.md     # Detailed county program info
├── tests/                      # Unit tests
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
└── README.md                   # This file
```

## County Coverage

### Honolulu County (Oahu) ✅ Fully Implemented
- **Dedication Periods**: 5-year (3% FMV), 10-year (1% FMV)
- **Volume**: ~1,400 dedications annually
- **Requirement**: ≥75% of usable land in agricultural use
- **Data Source**: RPAD PDFs + QPublic database

### Hawaii County (Big Island) 🔨 In Progress
- **Programs**: 3-year short-term, 10-year long-term, Community Food Sustainability
- **Requirement**: $2,000 minimum annual gross income
- **Recent Changes**: 2023 ordinance to prevent "gentleman farmer" abuse

### Maui County 🔨 In Progress
- **Dedication Periods**: 5-20 years (longer = greater discounts)
- **Tax Rate**: $5.74 per $1,000 assessed value
- **Deadline**: September 1 annually

### Kauai County 🔨 In Progress
- **Dedication Period**: 5-year commitment
- **Deadline**: July 1 annually
- **Recent Changes**: Ordinance No. 1132 (new petition required)

## Key Capabilities

### 1. PDF Data Extraction

Extract dedication data from annual RPAD reports:

```python
from ag_dedicated.extractors.pdf_extractor import PDFExtractor
from ag_dedicated import config

extractor = PDFExtractor(config)
df = extractor.process_all()  # Full pipeline: extract, merge, clean
```

### 2. Web Scraping

Scrape parcel details from county databases:

```python
from ag_dedicated.scrapers.honolulu import HonoluluScraper
from ag_dedicated import config

with HonoluluScraper(config) as scraper:
    parcel_data = scraper.scrape_parcel("1-2-3-4-5")  # TMK
```

### 3. Statute Comparison

Compare dedication programs across counties:

```python
from ag_dedicated.analysis.statute_comparison import StatuteComparison
from ag_dedicated import config

comparison = StatuteComparison(config)
report = comparison.generate_comparison_report()
print(report)
```

### 4. Data Validation

Validate TMK and petition numbers:

```python
from ag_dedicated.utils.validation import validate_tmk, validate_petition_number

is_valid = validate_tmk("1-2-3-4-5")
is_valid_petition = validate_petition_number("12345", numeric_only=True)
```

## Configuration

Edit `config/config.yaml` to customize:

- **Paths**: Data directories, output locations
- **County Settings**: URLs, dedication periods, assessment rates
- **Web Scraping**: Rate limits, timeouts, retry logic
- **Logging**: Log level, file output, rotation
- **Data Processing**: Year ranges, validation rules

## Data Pipeline

```
┌─────────────┐
│ PDF Reports │ (Annual RPAD reports 2013-2024)
└──────┬──────┘
       │ pdf_extractor.py
       ▼
┌─────────────┐
│  CSV Files  │ (One per year)
└──────┬──────┘
       │ merge_csv_files()
       ▼
┌─────────────┐
│   Merged    │ (All years combined)
└──────┬──────┘
       │ clean_petition_numbers()
       ▼
┌─────────────┐
│   Cleaned   │ (Validated records)
└──────┬──────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│QPublic Scrape│  │   Analysis   │
└──────────────┘  └──────────────┘
```

## Analysis Examples

See `notebooks/analysis.ipynb` for:

- **Temporal Trends**: Dedication volumes over time
- **Geographic Distribution**: TMK zone analysis
- **Statute Comparison**: Cross-county policy differences
- **Dedication Periods**: Distribution of 5yr vs 10yr commitments

## Legal Framework

### State Level
- **[Hawaii Revised Statutes §246-12](https://law.justia.com/codes/hawaii/2013/title-14/chapter-246/section-246-12)**: Statewide framework (established 1963)

### County Level
- **Honolulu**: [Revised Ordinances §8-7.3](https://codelibrary.amlegal.com/codes/honolulu/latest/honolulu/0-0-0-5936)
- **Hawaii**: [County website](https://hawaiipropertytax.com/)
- **Maui**: [County RPA](https://www.mauicounty.gov/1953/RPA-Forms-and-Instructions)
- **Kauai**: [Assessment office](https://www.kauai.gov/Government/Departments-Agencies/Finance/Real-Property-Tax/Assessment)

## Development

### Running Tests

```bash
pytest tests/ -v --cov=src/ag_dedicated
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

### Project Goals

**Completed:**
1. ✅ Compile historical dedication data (2013-2024)
2. ✅ Create modern Python package structure
3. ✅ Implement PDF extraction pipeline
4. ✅ Build Honolulu County web scraper
5. ✅ Develop statute comparison framework

**In Progress:**
3. 🔨 Collect tax data for all dedicated parcels
4. 🔨 Implement scrapers for Hawaii, Maui, Kauai counties

**Future:**
5. 📋 Map dedications geographically (GIS integration)
6. 📋 Quantify total tax benefits per county
7. 📋 Explore automated imagery analysis for compliance verification

## Migration from v1.0 (R-based)

**What Changed:**
- ✅ Full Python implementation (was R + Python hybrid)
- ✅ Multi-county support (was Honolulu only)
- ✅ Modern CLI tool (was manual script execution)
- ✅ Configuration management (was hardcoded paths)
- ✅ Comprehensive logging and error handling
- ✅ Data validation framework
- ✅ Statute comparison module

**Legacy Files:**
- `RPAD_Scraper.R` → `src/ag_dedicated/scrapers/honolulu.py`
- `pdf-scrape.py` → `src/ag_dedicated/extractors/pdf_extractor.py`
- `AG-Dedication.Rmd` → `notebooks/analysis.ipynb`

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Resources

- [Farmland Information Center](http://www.farmlandinfo.org) - Differential assessment policies
- [American Farmland Trust](https://www.farmland.org) - Agricultural land preservation
- [Hawaii State GIS](https://geoportal.hawaii.gov/) - Parcel and ownership data
- [County Real Property Offices](https://tax.hawaii.gov/geninfo/real-property-forms/) - Assessment information

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Real Property Assessment Division, City and County of Honolulu
- Howard Co. - "History and Provisions of the Agricultural Dedication Law in Hawaii" (1974)
- Glenn Michiaki Okimoto - "Optimal Control for Land Use Decisions in Hawaii" (1981)

## Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This is a research and analysis tool. Always consult with legal and tax professionals for specific property tax guidance.
