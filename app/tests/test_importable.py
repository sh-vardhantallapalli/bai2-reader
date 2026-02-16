"""Test Importable of BAI2 Reader"""

import importlib
import pytest


def test_src_importable():
    """Test importable"""
    try:
        from bai2_reader import BAI2Reader  # noqa: F401
    except ModuleNotFoundError:
        pytest.fail("Failed to Import BAI2 Reader")
    assert importlib.import_module("bai2_reader.ui"), "Failed to Import BAI2 Reader UI"
