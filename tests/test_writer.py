from unittest.mock import Mock, create_autospec

import pytest

from src.asockit import SocketWriter, WritableConnection


@pytest.fixture()
def connection() -> WritableConnection:
    return create_autospec(WritableConnection)


@pytest.fixture()
def sut(connection) -> SocketWriter:
    return SocketWriter(connection=connection)


@pytest.mark.asyncio()
class TestWrite:
    async def test_writes_data_to_connection(self, sut, connection) -> None:
        data = Mock()

        await sut.write(data)

        connection.writeline.assert_awaited_once_with(data)


@pytest.mark.asyncio()
class TestClose:
    async def test_closes_connection(self, sut, connection) -> None:
        await sut.close()

        connection.close.assert_awaited_once()
