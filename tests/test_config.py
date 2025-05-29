"""Tests for the anknote.config module."""

import json
import os
from pathlib import Path
from unittest.mock import patch
import pytest

from anknote.config import (
    AnknoteConfig,
    load_config,
    save_config,
    apply_env_overrides,
    create_default_config,
    get_config_path,
)


class TestAnknoteConfig:
    """Test the AnknoteConfig dataclass."""

    def test_default_config(self) -> None:
        """Test default configuration values."""
        config = AnknoteConfig()

        assert config.model == "gemini/gemini-2.0-flash-lite"
        assert config.max_retries == 3
        assert config.skip_readme is True
        assert config.file_extensions == [".md", ".markdown"]
        assert config.output_format == "tsv"
        assert config.escape_tabs is True
        assert config.log_level == "INFO"

    def test_from_dict(self) -> None:
        """Test creating config from dictionary."""
        data = {
            "model": "gpt-4",
            "max_retries": 5,
            "log_level": "DEBUG",
            "unknown_key": "should_be_ignored",
        }

        config = AnknoteConfig.from_dict(data)

        assert config.model == "gpt-4"
        assert config.max_retries == 5
        assert config.log_level == "DEBUG"
        # Unknown keys should be ignored, defaults should be used
        assert config.skip_readme is True

    def test_to_dict(self) -> None:
        """Test converting config to dictionary."""
        config = AnknoteConfig(model="test-model", max_retries=10)
        data = config.to_dict()

        assert data["model"] == "test-model"
        assert data["max_retries"] == 10
        assert "file_extensions" in data


class TestConfigLoading:
    """Test configuration loading and saving."""

    def test_load_nonexistent_config(self, tmp_path: Path) -> None:
        """Test loading config when file doesn't exist."""
        config_path = tmp_path / "nonexistent.json"
        config = load_config(config_path)

        # Should return default config
        assert config.model == "gemini/gemini-2.0-flash-lite"
        assert config.max_retries == 3

    def test_load_valid_config(self, tmp_path: Path) -> None:
        """Test loading valid config file."""
        config_path = tmp_path / "config.json"
        config_data = {
            "model": "custom-model",
            "max_retries": 7,
            "log_level": "WARNING",
        }

        with config_path.open("w") as f:
            json.dump(config_data, f)

        config = load_config(config_path)

        assert config.model == "custom-model"
        assert config.max_retries == 7
        assert config.log_level == "WARNING"

    def test_load_invalid_json(self, tmp_path: Path) -> None:
        """Test loading invalid JSON file."""
        config_path = tmp_path / "invalid.json"
        config_path.write_text("invalid json content")

        config = load_config(config_path)

        # Should return default config on parse error
        assert config.model == "gemini/gemini-2.0-flash-lite"

    def test_save_config(self, tmp_path: Path) -> None:
        """Test saving config to file."""
        config_path = tmp_path / "test_config.json"
        config = AnknoteConfig(model="test-model", max_retries=15)

        result = save_config(config, config_path)

        assert result is True
        assert config_path.exists()

        # Verify saved content
        with config_path.open() as f:
            data = json.load(f)

        assert data["model"] == "test-model"
        assert data["max_retries"] == 15


class TestEnvironmentOverrides:
    """Test environment variable overrides."""

    def test_apply_env_overrides(self) -> None:
        """Test applying environment variable overrides."""
        config = AnknoteConfig()

        with patch.dict(
            os.environ,
            {
                "ANKNOTE_MODEL": "env-model",
                "ANKNOTE_MAX_RETRIES": "10",
                "ANKNOTE_LOG_LEVEL": "DEBUG",
            },
        ):
            config = apply_env_overrides(config)

        assert config.model == "env-model"
        assert config.max_retries == 10
        assert config.log_level == "DEBUG"

    def test_invalid_env_override(self) -> None:
        """Test handling invalid environment variable values."""
        config = AnknoteConfig()

        with patch.dict(os.environ, {"ANKNOTE_MAX_RETRIES": "invalid_number"}):
            config = apply_env_overrides(config)

        # Should keep original value on invalid input
        assert config.max_retries == 3


class TestConfigPath:
    """Test configuration path resolution."""

    def test_get_config_path_local(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test getting config path when local config exists."""
        monkeypatch.chdir(tmp_path)
        local_config = tmp_path / ".anknote.json"
        local_config.write_text("{}")

        path = get_config_path()
        assert path == local_config

    def test_get_config_path_home(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test getting config path from home directory."""
        monkeypatch.setattr(Path, "home", lambda: tmp_path)

        # Create and change to a different directory
        other_dir = tmp_path / "other"
        other_dir.mkdir()
        monkeypatch.chdir(other_dir)  # Not in home directory

        home_config = tmp_path / ".config" / "anknote" / "config.json"
        home_config.parent.mkdir(parents=True)
        home_config.write_text("{}")

        path = get_config_path()
        assert path == home_config


def test_create_default_config() -> None:
    """Test creating default config string."""
    config_str = create_default_config()

    # Should be valid JSON
    data = json.loads(config_str)

    assert data["model"] == "gemini/gemini-2.0-flash-lite"
    assert data["max_retries"] == 3
    assert data["log_level"] == "INFO"
