from .abc import WritableConnection

__all__ = ["SocketWriter"]


class SocketWriter:
    """Writes lines to a connection."""

    __slots__ = ("_connection",)

    def __init__(self, connection: WritableConnection):
        """Initialize new instance with a connection.

        Args:
            connection (WritableConnection): The connection to send data to.
        """
        self._connection: WritableConnection = connection

    async def write(self, data: str) -> None:
        """Write text data over the connection.

        Args:
            data (str): Data to write over the connection.
        """
        await self._connection.writeline(data)

    async def close(self) -> None:
        """Close the underlying connection."""
        await self._connection.close()
