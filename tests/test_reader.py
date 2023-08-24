import asyncio
from unittest.mock import AsyncMock, create_autospec

import pytest

from src.asockit import (
    ReadableConnection,
    ReaderAlreadyStartedError,
    SocketReader,
    SocketReaderDelegate,
)


@pytest.fixture()
def connection() -> ReadableConnection:
    return create_autospec(ReadableConnection)


@pytest.fixture()
def delegate() -> SocketReaderDelegate:
    return create_autospec(SocketReaderDelegate)


@pytest.fixture()
def sut(connection) -> SocketReader:
    return SocketReader(connection=connection)


@pytest.mark.asyncio()
class TestStart:
    async def test_reads_lines_from_connection(self, sut, connection) -> None:
        await asyncio.wait_for(sut.start(), timeout=0.01)

        connection.readline.assert_awaited()

    async def test_when_delegate_set__calls_on_message_with_read_line(
        self, sut, connection, delegate
    ) -> None:
        sut.set_delegate(delegate)
        connection.readline = AsyncMock(return_value="foo")

        await asyncio.wait_for(sut.start(), timeout=0.01)

        delegate.on_message.assert_called_with("foo")

    async def test_when_starting_after_already_started__raises_error(
        self, sut, connection, delegate
    ) -> None:
        async def start_twice(reader: SocketReader) -> None:
            try:
                async with asyncio.TaskGroup() as group:
                    group.create_task(sut.start())
                    group.create_task(sut.start())
            except* ReaderAlreadyStartedError as excgroup:
                for exc in excgroup.exceptions:
                    raise exc

        with pytest.raises(ReaderAlreadyStartedError):
            await start_twice(sut)


@pytest.mark.asyncio()
class TestStop:
    async def test_after_stopping__is_reading_is_false(self, sut, connection) -> None:
        async def stop(reader: SocketReader) -> None:
            await asyncio.sleep(0)
            assert reader.is_reading

            await reader.stop()

            assert not reader.is_reading

        async with asyncio.TaskGroup() as group:
            group.create_task(sut.start())
            group.create_task(stop(sut))
