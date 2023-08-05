__all__ = ["ASerial"]


import asyncio
import serial  # type: ignore


class ASerial(serial.Serial):
    def __init__(self, port=None, baudrate=9600, *args, **kwargs):
        super().__init__(port, baudrate, timeout=0, *args, **kwargs)

    async def aread(self, size=1):
        buf = b""
        while len(buf) < size:
            buf += self.read(size - len(buf))
            await asyncio.sleep(0.01)
        return buf

    async def areadline(self, size=-1):
        buf = b""
        while not buf.endswith(b"\n") and (size < 0 or len(buf) < size):
            buf += self.readline(size - len(buf) if size >= 0 else -1)
            await asyncio.sleep(0.01)
        return buf

    async def areadlines(self, hint=-1):
        size = 0
        while hint < 0 or size < hint:
            s = await self.areadline()
            size += len(s)
            yield s
