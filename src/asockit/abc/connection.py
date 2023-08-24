from abc import abstractmethod
from typing import Any, Protocol

__all__ = ["WritableConnection", "ReadableConnection"]


class ConnectionClosedError(Exception):
    """Raised when a connection has closed."""

    def __init__(self, *args: Any):
        super().__init__("The connection has closed.")


class WritableConnection(Protocol):
    """A connection that can send data."""

    @abstractmethod
    async def writeline(self, line: str) -> None:
        """Send a text line over the connection.

        Args:
            line (str): The line to send.
        """


class ReadableConnection(Protocol):
    """A connection that can read data."""

    @abstractmethod
    async def readline(self) -> str:
        """Read a text line from the connection.

        Returns:
            The line read.

        Raises:
            ConnectionClosedError: Raised when the connection has closed.
        """
