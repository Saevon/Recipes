import asyncio
import concurrent
import threading


async def couroutine():
    pass

async def main():
    pass


'''md

Start:     [](https://docs.python.org/3/library/asyncio-task.html)
Debugging: [](https://docs.python.org/3/library/asyncio-dev.html)
Loop:      [](https://docs.python.org/3/library/asyncio-eventloop.html)
Blocking   [](https://docs.python.org/3/library/concurrent.futures.html)

Context-Manager [](https://www.python.org/dev/peps/pep-0492/)
Policies: [](https://docs.python.org/3/library/asyncio-policy.html)


Couroutine:  `async def` function

 * couroutine() is not scheduled/started until you also `await`
 * Can only await from one place
 * Doesn't return a future (returns a couroutine() instance)
    * .: cannot `.cancel()`

Task:
 * Wrapper around a function (usually a coroutine)
 * (is a future)
 * Usuallt auto-scheduled


Callback:
 * Sync non-blocking function
 * Runs inside the loop


Remember! unless you `await` anything you schedule cannot start yet
'''


# ------------------------------------------------------------------------------
# Running your Async
def quickstart():
    asyncio.run(main())


def starting_async():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    # Blocking
    loop.run_until_complete(couroutine())

    # In case you plan to add couroutines later
    loop.run_forever()


def start_coroutines(loop):
    '''
    Couroutines are `async def` functions
    '''
    future = loop.create_task(coroutine, *args, **kwargs)


def start_callbacks(loop):
    '''
    Callbacks are synchronous non-blocking? functions
    '''
    future = loop.call_soon(callback, *args, **kwargs)


def switching_to_sync(loop):
    '''
    `concurrent.futures` provides ways to convert futures to `sync blocking`

    '''
    # Run sync (uses a global threadpool)
    future = loop.run_in_executor(None, sync_func, *args)

    # Use an explicit pool
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = asyncio.gather(
            executor.submit(sync_func, *args, **kwargs),
            executor.submit(sync_func, *args, **kwargs),
            executor.submit(sync_func, *args, **kwargs),
        )

        # You can also use the loop function indirectly (Why though...)
        future = loop.run_in_executor(executor, sync_func, *args)

        # Run a bunch of things split up
        future = executor.map(sync_func, iter)

        # Blocking on futures
        future.wait()
        # Block when all are done
        [future for future in concurrent.futures.wait(future_or_futures_list_or_set)]
        # Block till the first one is done
        future = concurrent.futures.wait(futures, concurrent.futures.FIRST_COMPLETED)
        # Block until something breaks, or everything finishes
        future = concurrent.futures.wait(futures, concurrent.futures.FIRST_EXCEPTION)

        # Getting results (and raising any exceptions thrown)
        # WARNING! cancelled Tasks will break here with "InvalidStateError"
        future.result()




    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Same as the ThreadPool
        pass


# ------------------------------------------------------------------------------
def cancellation():
    # Tasks can be cancelled, or take too long
    async def helper():
        try:
            await couroutine()
        except asyncio.CancelledError:
            ''' Handle a timeout '''
        except asyncio.TimeoutError:
            ''' Handle a timeout '''

    # Note: Create a task to schedule the work, and be able to cancel
    future = asyncio.create_task(helper())

    future.cancel()

    # Cancelled tasks still run their callbacks
    future.add_done_callback(lambda future: future.cancelled() is True)

    try:
        result = await future
    except asyncio.CancelledError:
        # Sadly Cancellation error can still get here
        # BUT! only if theres async before/after the try or in th `except`
        result = None


async def cancellation_handling(loop):
    # Protect a couroutine from being cancelled by your parents:
    #   you will still get a cancellation error (and not get the results anymore)
    result = await asyncio.shield(couroutine())


    # Force a timeout on a task
    result = await asyncio.wait_for(couroutine(), timeout=1)
    # Block on couroutine (with timeout), BUT don't cancel the underlying task
    future = couroutine()
    result = await asyncio.wait_for(asyncio.shield(future), timeout=1)


def timeout():
    future = asyncio.create_task(couroutine())

    # Set a timeout
    future.wait_for(10)

    try:
        result = await future
    except asyncio.TimeoutError:
        result = None


# ------------------------------------------------------------------------------
# Concurrency
async def concurrency_async(loop):
    # Kick off a couroutine
    w1 = asyncio.create_task(coroutine())
    w2 = asyncio.create_task(coroutine())

    # You can make a heirarchy (by passing around futures)
    async def async_add(a1, a2):
        # But you must manually await them
        return await a1 + await a2

    w3 = asyncio.create_task(async_add(w1, w2))
    w4 = asyncio.create_task(async_add(w1, w3))
    w5 = asyncio.create_task(async_add(w2, w3))

    # BUT! Neither started yet... we need to give up your control first
    #    the first await would do it
    await asyncio.sleep(0)

    # IF we hadn't used `asyncio.create_task` they would start here (lazy evaluated)
    #    as we ask for each result, not as a batch
    # And we can now wait on them per-usual
    await w5 + w4

    # Kick off many couroutines and wait on them
    await asyncio.gather(
        coroutine(),
        coroutine(),
    )




# ------------------------------------------------------------------------------
# Scheduling

def sync_scheduling(p):
    future = loop.call_later(10, callback, *args, **kwargs)
    future = loop.call_at(time.time() + 10, callback, *args, **kwargs)


async def async_scheduling(loop):
    await loop.time()

    await asyncio.sleep(10)


async def periodic(func, seconds, loop=None, *args, **kwargs):
    '''
    Runs the task every X Seconds, regardless of how long the function takes to complete.

        async def couroutine(time_passed):
            pass

        periodic(couroutine, seconds=30, *args, **kwargs)

    If a scheduled time is missed, it will call the function with a larger delay
    '''
    if loop is None:
        loop = asyncio.get_event_loop()

    now = start = loop.time()

    while True:
        prev = now
        await asyncio.sleep(seconds - ((now - start) % seconds))

        now = loop.time()
        await func(now - prev, *args, **kwargs)




# ------------------------------------------------------------------------------
# Complex Features

def subprocess():
    '''
    ASYNCIO needs to be able to kill child-processes when tasks stop

    see Policies (link above)

    '''




# ------------------------------------------------------------------------------
# Threaded running

class AsyncLoopThread(threading.Thread):
    ''' Thread that runs an async code in an event loop


    When used as a context manager, it will ensure the loop spawns, then dies
    (it makes no guarantee about the underlying thread)

    with AsyncLoopThread() as async_thread:
        async_thread.schedule(my_future)
        async_thread.loop.



    UNTESTED CODE!!!!
    '''

    def __init__(self, loop=None):
        ''' Runs the given loop '''
        self.loop = loop
        self.shutdown = self.loop.create_future()

        super(AsyncLoopThread, self).__init__()

    def run(self):
        ''' Runs the event loop '''
        running = self.shutdown.set_running_or_notify_cancel()
        if not running():
            raise Exception("Loop already running?")

        self.loop.run_until_complete(self.shutdown)
        self.loop.close()

    def halt(self, timeout=0):
        '''
        Shutdown the event loop, returns whether the shutdown completed within the timeout.

        Calling this multiple times is safe.

        Set timeout to 0 for non-blocking
        '''
        self.shutdown.cancel()
        _, not_done = concurrent.futures.wait(self.shutdown, timeout=timeout)

        return len(not_done) == 0

    def schedule(self, future):
        ''' Schedules the future within its loop. Returns the wrapped future to wait on '''
        return asyncio.run_coroutine_threadsafe(future, loop=self.loop)

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, type, value, traceback):
        self.halt()














