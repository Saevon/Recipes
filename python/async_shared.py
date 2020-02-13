import functools


class AsyncEvent(object):
    ''' A partial call, ready to be applied '''

    def __init__(self, sync_func, async_func, args, kwargs):
        ''' Stores the partial info '''
        self.sync_func = sync_func
        self.async_func = async_func
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return 'AsyncEvent({})'.format(self.sync_func.__name__)


class async_handler(object):
    ''' Decorator that can be run either async/blocking '''

    def __init__(self, func, async_func=None):
        ''' Creates an implementation that can run either blocking/async '''
        self.sync_func = func
        self.async_func = async_func
        if self.async_func is None:
            def not_implemented(*args, **kwargs):
                raise NotImplementedError("No Async Version")
            self.async_func = not_implemented

    def register_async(self, func):
        ''' Adds an async function '''
        self.async_func = func

    def __call__(__self, *args, **kwargs):
        '''
        Use like a normal function, with yield
            result = (yield func(args))

        Generates an AsyncEvent that will be run in the trampoline
        '''
        return AsyncEvent(
            sync_func=__self.sync_func,
            async_func=__self.async_func,
            args=args,
            kwargs=kwargs,
        )

    def __get__(self, instance, owner):
        ''' Fix problems with instance methods '''
        return functools.partial(self.__call__, instance)


def sync_shared(coroutine_init):
    '''
    Creates a function that can be used for blocking and async code
    '''

    @functools.wraps(coroutine_init)
    def wrapper_sync(*args, **kwargs):
        ''' Blocking (Synchronous) Trampoline '''
        coroutine = coroutine_init(*args, **kwargs)

        try:
            # Initialize the coroutine
            event = coroutine.send(None)

            while True:
                if not isinstance(event, AsyncEvent):
                    event = coroutine.throw(TypeError("Invalid AsyncEvent request yielded"))
                    continue

                try:
                    result = event.sync_func(*event.args, **event.kwargs)
                except BaseException as error:
                    event = coroutine.throw(error)
                else:
                    event = coroutine.send(result)
        except StopIteration as error:
            return error.value

    @functools.wraps(coroutine_init)
    async def wrapper_async(*args, **kwargs):
        ''' Asynchronous Trampoline '''
        coroutine = coroutine_init(*args, **kwargs)
        event = next(coroutine)

        try:
            while True:
                if not isinstance(event, AsyncEvent):
                    event = coroutine.throw(TypeError("Invalid AsyncEvent request yielded"))
                    continue

                try:
                    result = await event.async_func(*event.args, **event.kwargs)
                except BaseException as error:
                    event = coroutine.throw(error)
                else:
                    event = coroutine.send(result)
        except StopIteration as error:
            return error.value

    wrapper_sync.run_async = wrapper_async
    wrapper_sync.aevent = async_handler(
        wrapper_sync,
        async_func=wrapper_async,
    )

    return wrapper_sync
