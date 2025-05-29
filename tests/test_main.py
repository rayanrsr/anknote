"""Tests for the main anknote module."""

import pytest
from anknote import __version__, main


def test_version():
    """Test that version is defined."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_main_function():
    """Test that main function runs without error."""
    # This should not raise an exception
    main() 