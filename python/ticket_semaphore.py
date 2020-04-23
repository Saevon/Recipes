import contextlib
import multiprocessing
import time
import ctypes


class Ticket():
    ''' A ticket from a TicketSemaphore '''
    def __init__(self, ticketer, size):
        self.size = size
        self.ticketer = ticketer

    def release(self, *args, **kwargs):
        ''' Releases this ticket from the owning ticketer '''
        self.ticketer.release(self, *args, **kwargs)


class TicketSemaphore():
    '''
    Semaphore that allows grabbing different size of product

    ticketer = TicketSemaphore(10)

    ticket = ticketer.acquire(3)
    ticket.release()

    with ticketer(size=3):
        pass
    '''

    def __init__(self, size):
        self.available = multiprocessing.Value(ctypes.c_int)
        self.size = size
        self.lock = multiprocessing.Condition()

    def acquire(self, timeout=None, size=1):
        ''' Grabs a ticket of the given size '''
        time_left = None
        if timeout:
            start = time.time()
            time_left = timeout

        self.lock.acquire(timeout=time_left)

        # Wait until there is enough space
        while self.available < size:
            if timeout:
                time_left = timeout - (time.time() - start)

            try:
                self.lock.wait(timeout=time_left)
            except RuntimeError:
                # We've run out of time
                return False

        # The ticket is ours!
        self.available -= size

        return Ticket(self, size)

    def release(self, ticket):
        ''' Releases the given ticket '''
        with self.lock:
            self.available += ticket.size
            if self.available >= self.size:
                raise OverflowError("Too many tickets returned")

    def __call__(self, **kwargs):
        ''' ContextManager with arguments '''
        @contextlib.contextmanager
        def with_ticket_lock():
            try:
                ticket = self.acquire(**kwargs)
                yield ticket
            finally:
                if ticket:
                    ticket.release()



