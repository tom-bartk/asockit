<div align="center">
  <a href="https://github.com/tom-bartk/asockit">
    <img src="https://asockit.tombartk.com/images/logo.png" alt="Logo" width="358" height="99">
  </a>

<div align="center">
<a href="https://jenkins.tombartk.com/job/asockit/">
  <img alt="Jenkins" src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Fasockit">
</a>
<a href="https://jenkins.tombartk.com/job/asockit/lastCompletedBuild/testReport/">
  <img alt="Jenkins tests" src="https://img.shields.io/jenkins/tests?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Fasockit">
</a>
<a href="https://jenkins.tombartk.com/job/asockit/lastCompletedBuild/coverage/">
  <img alt="Jenkins Coverage" src="https://img.shields.io/jenkins/coverage/apiv4?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Fasockit%2F">
</a>
<a href="https://www.gnu.org/licenses/agpl-3.0.en.html">
  <img alt="PyPI - License" src="https://img.shields.io/pypi/l/asockit">
</a>
<a href="https://pypi.org/project/asockit/">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/asockit">
</a>
<a href="https://pypi.org/project/asockit/">
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/asockit">
</a>
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;"></a>
</div>

  <p align="center">
    Client-side toolkit for async sockets.
    <br />
    <a href="https://asockit.tombartk.com"><strong>Documentation</strong></a>
  </p>
</div>

## Simple example

### Reading from a socket

```python3
# reading.py

import asyncio

from asockit import AsyncioReadableConnection, ConnectionClosedError, SocketReader


class SocketReaderDelegate:
    def on_message(self, message: str) -> None:
        print(f'[SocketReaderDelegate] Received message "{message}"')


async def main() -> None:
    stream_reader, _ = await asyncio.open_connection("localhost", port=3000)

    reader = SocketReader(
        connection=AsyncioReadableConnection(reader=stream_reader)
    )

    delegate = SocketReaderDelegate()
    reader.set_delegate(delegate)

    try:
        await reader.start()
    except ConnectionClosedError:
        print("The connection has closed.")


if __name__ == "__main__":
    asyncio.run(main())
```

```sh
$ nc -lnp 3000 -c 'echo -n "Hello\nWorld!\n"'

# In a different shell session
$ python3 reading.py

[SocketReaderDelegate] Received message "Hello"
[SocketReaderDelegate] Received message "World!"
The connection has closed.
```

### Writing to a socket

```python3
# writing.py

import asyncio

from asockit import AsyncioWritableConnection, SocketWriter


async def main() -> None:
    _, stream_writer = await asyncio.open_connection("localhost", port=3000)

    writer = SocketWriter(
        connection=AsyncioWritableConnection(writer=stream_writer)
    )

    await writer.write("Hello world!\n")


if __name__ == "__main__":
    asyncio.run(main())
```

```sh
$ python3 writing.py

# Started before running the script
$ nc -lvnp 3000

listening on [any] 3000 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 41560
Hello world!
```

## Installation

Asockit is available as [`asockit`](https://pypi.org/project/asockit/) on PyPI:

```shell
pip install asockit
```

## Usage

For detailed quickstart and API reference, visit the [Documentation](https://asockit.tombartk.com/quickstart/).


## License
![AGPLv3](https://www.gnu.org/graphics/agplv3-with-text-162x68.png)
```monospace
Copyright (C) 2023 tombartk 

This program is free software: you can redistribute it and/or modify it under the terms
of the GNU Affero General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.
If not, see https://www.gnu.org/licenses/.
```
