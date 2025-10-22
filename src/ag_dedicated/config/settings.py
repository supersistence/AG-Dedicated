"""Configuration management for ag-dedicated."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Settings:
    """
    Configuration settings loaded from config.yaml.

    Provides convenient access to configuration values with support
    for environment variable overrides.
    """

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        """Singleton pattern to ensure single config instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        # Find project root (where config/ directory is)
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent.parent

        config_path = project_root / "config" / "config.yaml"

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at {config_path}. "
                "Please ensure config/config.yaml exists in project root."
            )

        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)

        # Store project root for path resolution
        self._project_root = project_root

    @property
    def project_root(self) -> Path:
        """Get project root directory."""
        return self._project_root

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.

        Args:
            key: Configuration key in dot notation (e.g., 'paths.data.raw')
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            >>> config = Settings()
            >>> config.get('counties.honolulu.name')
            'City and County of Honolulu'
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_path(self, key: str) -> Path:
        """
        Get absolute path from configuration.

        Args:
            key: Path key in dot notation (e.g., 'paths.data.raw')

        Returns:
            Absolute Path object
        """
        relative_path = self.get(key)
        if relative_path is None:
            raise ValueError(f"Path not found in config: {key}")

        return (self.project_root / relative_path).resolve()

    def get_county_config(self, county: str) -> Dict[str, Any]:
        """
        Get configuration for specific county.

        Args:
            county: County name (honolulu, hawaii, maui, kauai)

        Returns:
            County configuration dictionary
        """
        config = self.get(f'counties.{county.lower()}')
        if config is None:
            raise ValueError(f"Unknown county: {county}")
        return config

    def get_enabled_counties(self) -> list[str]:
        """Get list of enabled counties."""
        counties = self.get('counties', {})
        return [
            name for name, cfg in counties.items()
            if cfg.get('enabled', False)
        ]

    def __getitem__(self, key: str) -> Any:
        """Allow dict-like access: config['key']."""
        value = self.get(key)
        if value is None:
            raise KeyError(f"Configuration key not found: {key}")
        return value

    def __contains__(self, key: str) -> bool:
        """Check if key exists in configuration."""
        return self.get(key) is not None

    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get('logging.level', 'INFO')

    @property
    def data_dir(self) -> Path:
        """Get processed data directory."""
        return self.get_path('paths.data.processed')

    @property
    def raw_data_dir(self) -> Path:
        """Get raw data directory."""
        return self.get_path('paths.data.raw')

    @property
    def dedication_history_dir(self) -> Path:
        """Get dedication history directory."""
        return self.get_path('paths.dedication_history')

    def ensure_directories(self) -> None:
        """Create all configured directories if they don't exist."""
        paths_to_create = [
            'paths.data.raw',
            'paths.data.processed',
            'paths.data.statutes',
            'paths.output',
            'paths.notebooks',
            'paths.logs',
        ]

        for path_key in paths_to_create:
            try:
                path = self.get_path(path_key)
                path.mkdir(parents=True, exist_ok=True)
            except ValueError:
                # Path not in config, skip
                pass
