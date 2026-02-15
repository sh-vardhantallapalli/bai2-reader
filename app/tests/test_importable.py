"""Test Importable of BAI2 Reader"""

import importlib

assert importlib.import_module("src.bai2_reader"), "Failed to Import BAI2 Reader"
assert importlib.import_module("src.ui"), "Failed to Import BAI2 Reader UI"

print("Success!")
