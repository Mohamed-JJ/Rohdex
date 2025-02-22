from rich.console import Console
from rich.logging import RichHandler
import logging
from functools import lru_cache


class LoggerSingleton:
    _instance = None
    _console = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._setup_logger()
        return cls._instance

    @classmethod
    def _setup_logger(cls):
        cls._console = Console()
        logging.basicConfig(
            level="INFO",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(console=cls._console, rich_tracebacks=True)],
        )
        cls._logger = logging.getLogger("rich")

    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            cls()
        return cls._logger

    @classmethod
    def get_console(cls):
        if cls._instance is None:
            cls()
        return cls._console


@lru_cache()
def get_logger():
    """Get cached logger instance."""
    return LoggerSingleton.get_logger()
