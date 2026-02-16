"""Exceptions for Bai2Reader"""


class Bai2ReaderException(Exception):
    """Base exception for Bai2Reader"""


class InvalidFileFormatException(Bai2ReaderException):
    """Raised when the input file format is invalid"""


class UnknownValueException(Bai2ReaderException):
    """Raised when an unknown value is encountered in the BAI2 file"""
