import asyncio
from abc import abstractmethod
from contextlib import suppress
from typing import Protocol
from weakref import ReferenceType, ref

from .abc import ReadableConnection

__all__ = ["ReaderAlreadyStartedError", "SocketReader", "SocketReaderDelegate"]


class ReaderAlreadyStartedError(Exception):
    """Raised when attempting to start an already started `SocketReader`."""

    def __init__(self):
        super().__init__("SocketReader has already started reading.")


class SocketReaderDelegate(Protocol):
    """The delegate of the socket reader."""

    @abstractmethod
    def on_message(self, message: str) -> None:
        """Callback called when the `SocketReader` has read a line.

        Args:
            message (str): The read line.
        """


class SocketReader:
    """Reads lines from a connection."""

    __slots__ = ("_connection", "_task", "_delegate", "_is_reading", "__weakref__")

    @property
    def is_reading(self) -> bool:
        """Return whether the reader is currently reading from the connection."""
        return self._is_reading

    def __init__(self, connection: ReadableConnection):
        """Initialize new instance with a connection.

        Args:
            connection (ReadableConnection): The connection to read lines from.
        """
        self._connection: ReadableConnection = connection
        self._is_reading: bool = False
        self._task: asyncio.Task | None = None
        self._delegate: ReferenceType[SocketReaderDelegate] | None = None

    async def start(self) -> None:
        """Start reading data from the connection.

        Data is read one line at a time. If a `SocketReaderDelegate` is set,
        the `on_message` method is called for every line read.

        To stop reading, await the `stop` coroutine.

        Raises:
            ReaderAlreadyStartedError: Raised when the reader has already started reading.
            ConnectionClosedError: Raised when the connection has closed.
        """
        if not self._is_task_running():
            self._is_reading = True
            self._task = asyncio.create_task(self._start_reading())
            await self._task
        else:
            raise ReaderAlreadyStartedError()

    async def stop(self) -> None:
        """Stop reading data from the connection.

        Sets the internal reading `asyncio.Task` as cancelled, and awaits it
        until completed. Does nothing if not currently reading.
        """
        if self._task:
            self._is_reading = False
            self._task.cancel()
            await self._task

    def set_delegate(self, delegate: SocketReaderDelegate) -> None:
        """Store a weak reference to the `delegate`.

        Args:
            delegate (SocketReaderDelegate): The delegate to store.
        """
        self._delegate = ref(delegate)

    async def _start_reading(self) -> None:
        """Read lines from the connection in an infinite loop."""
        with suppress(asyncio.CancelledError):
            delegate: SocketReaderDelegate | None = (
                self._delegate() if self._delegate else None
            )
            while True:
                message = await self._connection.readline()
                if not delegate:
                    delegate = self._delegate() if self._delegate else None
                if delegate:
                    delegate.on_message(message)
                await asyncio.sleep(0)

    def _is_task_running(self) -> bool:
        """Check if reading task is running.

        Task is running when it's not `None`, and is not cancelled or
        not actively being cancelled.

        Returns:
            `True` if task is running; `False`, otherwise.
        """
        task: asyncio.Task | None = self._task
        if task:
            return not (task.cancelled() or task.cancelling())
        return False
