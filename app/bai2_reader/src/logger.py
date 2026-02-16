"""Base logger configuration for the application."""

__all__ = ["BaseLogger", "log"]


import logging


class BaseLogger:
    """Base logger configuration class."""

    def __init__(
        self,
        name: str = __name__,
        log_level: int = logging.INFO,
        log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ):
        """Initializes the BaseLogger with the specified configuration."""
        self.log = logging.getLogger(name)
        self.log.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)

        if not self.log.hasHandlers():
            self.log.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        """Returns the configured logger instance."""
        return self.log


log = BaseLogger(name="bai2-reader").get_logger()
