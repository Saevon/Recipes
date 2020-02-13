from async_shared import async_handler, sync_shared

# Async Creep

# ------------------------------------------------------------------------------
# Ways to handle it

# Writing Blocking primary code
#   * Spin off ProcessPool or ThreadPool
#   * But now you cannot get any async benefits (max blocking calls equals the number of threads)

# Writing Async primary code
#   * Create a event_loop
#   * BUT now you need to import all the async libraries in both cases
#   (Ideally it would be optional)

# Writing Both
#   * not DRY

# ------------------------------------------------------------------------------
# Example code
#
# Note: 'with' does not work (if you need blocking/async contextmanagers)

try:
    import aiofiles
    import asyncio
    import fcntl
except ImportError:
    logger.debug('Async Disabled')

import time
import os
import json

# Polyfill
# Not yet in aiofiles
aiofiles.path = object()
aiofiles.path.exists = aiofiles.os.wrap(os.path.exists)

# ------------------------------------------------------------------------------
# Create the mixed function calls
@async_handler
def sys_random(num_bytes):
    return os.urandom(num_bytes)


@sys_random.register_async
async def sys_random_async(num_bytes):
    async with aiofiles.open('/dev/urandom', 'rb') as rand_fh:
        # Pretend its that easy to open a non-blocking file :)
        rand_fh.non_blocking = True
        while True:
            data = await rand_fh.read(num_bytes)
            if len(data) >= num_bytes:
                return data
            await asyncio.sleep(0.1)


@async_handler
def os_exists(path):
    return os.path.exists(path)


@os_exists.register_async
async def os_exists_async(path):
    return aiofiles.path.exists(path)


@async_handler
def sys_sleep(seconds):
    time.sleep(seconds)


@sys_sleep.register_async
async def sys_sleep_async(seconds):
    await asyncio.sleep(seconds)


class AsyncableFile():
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

        self.fh = None

    def _open_if_needed(self):
        if self.fh:
            return
        self.fh = open(self.filename, self.mode)

    async def _open_if_needed_async(self):
        if self.fh:
            return
        self.fh = await aiofiles.open(self.filename, self.mode)

    @async_handler
    def read(self):
        self._open_if_needed()
        return self.fh.read()

    @read.register_async
    async def read_async(self):
        await self._open_if_needed_async()
        return await self.fh.read()

    @async_handler
    def close(self):
        if self.fh:
            self.fh.close()

    @close.register_async
    async def close_async(self):
        if self.fh:
            await self.fh.close()


# --------------------------------------------------------------------------------------------------


@sync_shared
def read_id(filepath):
    if not (yield os_exists(filepath)):
        raise Exception("File doesn't exist")

    # Decomposed "With", since its not supported
    file = AsyncableFile(filepath, 'r')

    try:
        raw_data = yield file.read()
    finally:
        yield file.close()
    # END Decomposed

    print(raw_data)

    data = json.loads(raw_data)
    keyid = data.get('id', None)

    assert isinstance(keyid, int)

    return keyid


@sync_shared
def main(filepath):
    ''' '''
    print('sleeping')
    yield sys_sleep(0.1)

    keyid = (yield read_id.aevent(filepath))

    folder = os.path.dirname(filepath)
    keyfile = os.path.join(folder, 'keyfile_{}.json'.format(keyid))
    print(keyfile)

    if not (yield os_exists(keyfile)):
        raise Exception("No Keyfile exists")

    print('sleeping')
    yield sys_sleep(0.1)

    # Pretend we do something with that keyfile
    print((yield sys_random(4)))


# Example traceback
'''
Traceback (most recent call last):
  File "main.py", line 257, in <module>
    main('tmp.txt')
  File "async_shared.py", line 56, in wrapper_sync
    event = coroutine.send(result)
  File "main.py", line 246, in main
    raise Exception("No Keyfile exists")
'''

if __name__ == '__main__':
    print('========')
    print("Synchronous")
    main('tmp.txt')

    print('========')
    print("Asynchronous")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main.run_async('tmp.txt'))
    finally:
        loop.close()
