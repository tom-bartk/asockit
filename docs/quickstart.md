## Reading from a socket

### Define the Delegate

A [`SocketReaderDelegate`](/api/reader/#asockit.SocketReaderDelegate) is the receiver of lines that the reader will read. It's a protocol, so no need for subclassing anything: 

```python3
class MySocketReaderDelegate:
    def on_message(self, message: str) -> None:
        print(f'[SocketReaderDelegate] Received message "{message}"')
```

### Open a Connection

Create a [`ReadableConnection`](/api/connection/#asockit.abc.ReadableConnection) using the [`AsyncioReadableConnection`](/api/connection/#asockit.AsyncioReadableConnection), which is a handy wrapper over the [`asyncio.StreamReader`](https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamReader):

```python3
import asockit


async def main() -> None:
    stream_reader, _ = await asyncio.open_connection("localhost", port=3000)

    connection = asockit.AsyncioReadableConnection(reader=stream_reader)
```

### Create the Reader

A [`SocketReader`](/api/reader/#asockit.SocketReader) reads text lines from the [`ReadableConnection`](/api/connection/#asockit.abc.ReadableConnection) and "feeds" them to the [`SocketReaderDelegate`](/api/reader/#asockit.SocketReaderDelegate):

```python3
import asockit


async def main() -> None:
    ...

    reader = asockit.SocketReader(connection=connection)

    delegate = MySocketReaderDelegate()
    reader.set_delegate(delegate)
```

### Start reading

Await the [`start`](/api/reader/#asockit.reader.SocketReader.start) coroutine to start reading lines until the [`stop`](/api/reader/#asockit.reader.SocketReader.stop) coroutine is awaited, or the connection closes.

```python3
import asockit


async def main() -> None:
    ...

    try:
        await reader.start()
    except asockit.ConnectionClosedError:
        print("The connection has closed.")
```

```sh
$ nc -lnp 3000 -c 'echo "Hello\nWorld!\n"'

# In a different shell session
$ python3 main.py

[SocketReaderDelegate] Received message "Hello"
[SocketReaderDelegate] Received message "World!"
The connection has closed.
```

## Writing to a socket

### Open a Connection

Open a [`WritableConnection`](/api/connection/#asockit.abc.WritableConnection) by creating an [`AsyncioWritableConnection`](/api/connection/#asockit.AsyncioWritableConnection), which is a useful wrapper over the [`asyncio.StreamWriter`](https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamWriter):

```python3
import asockit


async def main() -> None:
    _, stream_writer = await asyncio.open_connection("localhost", port=3000)

    connection = asockit.AsyncioWritableConnection(writer=stream_writer)
```

### Create the Writer

A [`SocketWriter`](/api/writer/#asockit.SocketWriter) writes text lines to the [`WritableConnection`](/api/connection/#asockit.abc.WritableConnection): 

```python3
import asockit


async def main() -> None:
    ...

    writer = asockit.SocketWriter(connection=connection)
```

### Write a line

Pass your payload to the [`write`](/api/writer/#asockit.writer.SocketReader.write) coroutine to send it over the connection:

```python3
async def main() -> None:
    ...

    await writer.write("Hello world!\n")
```

```sh
$ python3 main.py

# Started before running the script
$ nc -lvnp 3000

listening on [any] 3000 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 41560
Hello world!
```

<hr/>
To learn more, see the [API Documentation](/api/reader/).
<br/>
