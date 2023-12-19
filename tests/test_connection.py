import asyncio
from unittest.mock import AsyncMock, Mock, call, create_autospec

import pytest

from src.asockit import (
    AsyncioReadableConnection,
    AsyncioWritableConnection,
    ConnectionClosedError,
)


@pytest.fixture()
def reader() -> asyncio.StreamReader:
    reader = create_autospec(asyncio.StreamReader)
    reader.readline = AsyncMock(return_value=b"foo\n")
    reader.at_eof = Mock(return_value=False)
    return reader


@pytest.fixture()
def writer() -> asyncio.StreamWriter:
    return create_autospec(asyncio.StreamWriter)


@pytest.fixture()
def writable_sut(writer) -> AsyncioWritableConnection:
    return AsyncioWritableConnection(writer=writer)


@pytest.fixture()
def readable_sut(reader) -> AsyncioReadableConnection:
    return AsyncioReadableConnection(reader=reader)


@pytest.mark.asyncio()
class TestAsyncioWritableConnection:
    async def test_writeline__writes_bytes_to_writer(self, writable_sut, writer) -> None:
        await writable_sut.writeline("foo")

        writer.write.assert_called_once_with(b"foo\n")

    async def test_writeline__drains_writer_after_writing(
        self, writable_sut, writer
    ) -> None:
        await writable_sut.writeline("foo")

        assert writer.mock_calls == [call.write(b"foo\n"), call.drain()]

    async def test_writeline__strips_extra_newlines(self, writable_sut, writer) -> None:
        await writable_sut.writeline("\n\nfoo\n\n\n")

        writer.write.assert_called_once_with(b"foo\n")

    async def test_writeline__when_input_has_many_lines__calls_write_for_each_line(
        self, writable_sut, writer
    ) -> None:
        expected_calls = [call(b"foo\n"), call(b"bar\n"), call(b"baz\n")]

        await writable_sut.writeline("foo\nbar\nbaz")

        writer.write.assert_has_calls(expected_calls)

    async def test_writeline__when_input_has_many_lines__does_not_send_empty_lines(
        self, writable_sut, writer
    ) -> None:
        expected_calls = [call(b"foo\n"), call(b"bar\n"), call(b"baz\n")]

        await writable_sut.writeline("\n  \nfoo\nbar\n \n\nbaz\n\n")

        writer.write.assert_has_calls(expected_calls)

    async def test_close__closes_writer(self, writable_sut, writer) -> None:
        await writable_sut.close()

        writer.close.assert_called_once()
        writer.wait_closed.assert_awaited_once()


@pytest.mark.asyncio()
class TestAsyncioReadableConnection:
    async def test_readline__reads_line_from_reader(self, readable_sut, reader) -> None:
        await readable_sut.readline()

        reader.readline.assert_awaited_once()

    async def test_readline__returns_decoded_string(self, readable_sut) -> None:
        expected = "foo"

        result = await readable_sut.readline()

        assert result == expected

    async def test_when_connection_at_eof__throws_connection_closed_error(
        self, readable_sut, reader
    ) -> None:
        reader.at_eof = Mock(return_value=True)

        with pytest.raises(ConnectionClosedError):
            await readable_sut.readline()
