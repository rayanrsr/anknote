"""Configuration management for Anknote."""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import json
from dataclasses import dataclass, asdict

from loguru import logger


@dataclass
class AnknoteConfig:
    """Configuration settings for Anknote."""

    # AI Model settings
    model: str = "gemini/gemini-2.0-flash-lite"
    max_retries: int = 3

    # File processing settings
    skip_readme: bool = True
    file_extensions: Optional[list[str]] = None

    # Output settings
    output_format: str = "tsv"
    escape_tabs: bool = True

    # Logging settings
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        """Set default values after initialization."""
        if self.file_extensions is None:
            self.file_extensions = [".md", ".markdown"]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnknoteConfig":
        """Create config from dictionary."""
        # Filter out unknown keys
        valid_keys = {field.name for field in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)


def get_config_path() -> Path:
    """Get the path to the configuration file."""
    # Check for config in current directory first
    local_config = Path.cwd() / ".anknote.json"
    if local_config.exists():
        return local_config

    # Check for global config in user home directory
    home_config = Path.home() / ".config" / "anknote" / "config.json"
    if home_config.exists():
        return home_config

    # Check for XDG config directory
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        xdg_config_path = Path(xdg_config) / "anknote" / "config.json"
        if xdg_config_path.exists():
            return xdg_config_path

    # Return default location (may not exist)
    return home_config


def load_config(config_path: Optional[Path] = None) -> AnknoteConfig:
    """
    Load configuration from file or return default.

    Args:
        config_path: Optional path to config file

    Returns:
        AnknoteConfig object
    """
    if config_path is None:
        config_path = get_config_path()

    if not config_path.exists():
        logger.debug(f"No config file found at {config_path}, using defaults")
        return AnknoteConfig()

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        config = AnknoteConfig.from_dict(data)
        logger.debug(f"Loaded config from {config_path}")
        return config

    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Failed to parse config file {config_path}: {e}")
        logger.info("Using default configuration")
        return AnknoteConfig()
    except Exception as e:
        logger.error(f"Error loading config file {config_path}: {e}")
        return AnknoteConfig()


def save_config(config: AnknoteConfig, config_path: Optional[Path] = None) -> bool:
    """
    Save configuration to file.

    Args:
        config: Configuration to save
        config_path: Optional path to save to

    Returns:
        True if successful, False otherwise
    """
    if config_path is None:
        config_path = get_config_path()

    try:
        # Create directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with config_path.open("w", encoding="utf-8") as f:
            json.dump(config.to_dict(), f, indent=2)

        logger.info(f"Saved config to {config_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to save config to {config_path}: {e}")
        return False


def create_default_config() -> str:
    """Create a default configuration file content."""
    config = AnknoteConfig()
    return json.dumps(config.to_dict(), indent=2)


# Environment variable overrides
def apply_env_overrides(config: AnknoteConfig) -> AnknoteConfig:
    """Apply environment variable overrides to config."""
    env_mappings = {
        "ANKNOTE_MODEL": "model",
        "ANKNOTE_MAX_RETRIES": "max_retries",
        "ANKNOTE_LOG_LEVEL": "log_level",
    }

    for env_var, config_key in env_mappings.items():
        value = os.environ.get(env_var)
        if value is not None:
            # Convert to appropriate type
            if config_key == "max_retries":
                try:
                    converted_value = int(value)
                    setattr(config, config_key, converted_value)
                except ValueError:
                    logger.warning(f"Invalid value for {env_var}: {value}")
                    continue
            else:
                setattr(config, config_key, value)

            logger.debug(
                f"Applied environment override: {config_key} = {getattr(config, config_key)}"
            )

    return config
