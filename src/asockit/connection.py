from asyncio import StreamReader, StreamWriter

from .abc import ConnectionClosedError, ReadableConnection, WritableConnection

__all__ = ["AsyncioReadableConnection", "AsyncioWritableConnection"]


class AsyncioReadableConnection(ReadableConnection):
    """A readable connection wrapping an `asyncio.StreamReader`."""

    __slots__ = ("_reader",)

    def __init__(self, reader: StreamReader):
        """Initialize new read connection with a stream reader.

        Args:
            reader (StreamReader): The reading wrapper over a stream.
        """
        self._reader: StreamReader = reader

    async def readline(self) -> str:
        """Read a text line from the connection.

        Returns:
            The line read.

        Raises:
            ConnectionClosedError: Raised when the connection has closed.
        """
        if self._reader.at_eof():
            raise ConnectionClosedError()

        message = await self._reader.readline()
        return message.decode().strip()


class AsyncioWritableConnection(WritableConnection):
    """A writable connection wrapping an `asyncio.StreamWriter`."""

    __slots__ = ("_writer",)

    def __init__(self, writer: StreamWriter):
        """Initialize new write connection with a stream writer.

        Args:
            writer (StreamWriter): The writing wrapper over a stream.
        """
        self._writer: StreamWriter = writer

    async def writeline(self, line: str) -> None:
        """Send a text line over the connection.

        The input text is split into a list of lines. Each line has its whitespace
        characters stripped and a single newline character appended.
        Then, every line is sent separately over the connection.

        Args:
            line (str): The line to send.
        """
        lines = [line_.strip() for line_ in line.splitlines()]
        for line in lines:
            if line:
                self._writer.write(f"{line}\n".encode())
                await self._writer.drain()
