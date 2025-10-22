"""Setup script for ag-dedicated package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="ag-dedicated",
    version="2.0.0",
    description="Analysis of Hawaii's agricultural property tax dedication system across all counties",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AG-Dedicated Project",
    author_email="",
    url="https://github.com/yourusername/AG-Dedicated",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "tabula-py>=2.8.0",
        "PyPDF2>=3.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "rich>=13.5.0",
        "tqdm>=4.66.0",
        "loguru>=0.7.0",
        "pydantic>=2.4.0",
        "tenacity>=8.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "isort>=5.12.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "ipykernel>=6.25.0",
            "notebook>=7.0.0",
            "plotly>=5.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ag-dedicated=ag_dedicated.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="agriculture, property-tax, hawaii, data-analysis, public-policy",
)
