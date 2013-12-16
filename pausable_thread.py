from contextlib import contextmanager

import threading


class PausableThread(threading.Thread):
    '''
    A Thread that can be paused, but only at point convinient for it

    a parent (singular only) can request a pause, and the child will then
    pause when it reaches a pause_point()


    Sub-Classes should use the run method as usual for their code
    '''

    def __init__(self):
        super(PausableThread, self).__init__()

        self.__pause_request = False
        self.__action = threading.Condition()

    def pause(self):
        '''
        Tells the thread to pause itself, sleeping until it does so

        If the thread isn't alive, this will return False (without blocking)
        '''
        # Set the pause request
        with self.__action:
            # Make sure the thread is alive
            if not self.is_alive():
                return False

            # Make sure the pause request is set
            self.__pause_request = True

            # Wait for a return
            self.__action.wait()

        return True

    def __stop(self):
        # First make sure the thread is actually stopped
        # Note: this isn't technically public Thread stuff
        value = super(PausableThread, self).__stop()

        # Make sure to now wake anyone who might have begun to wait
        # before the thread was stopped
        with self.__action:
            self.__action.notify_all()

        # Make sure the return value is the same as the original one
        return value


    def resume(self):
        '''
        Tells the thread to resume its work
        '''
        with self.__action:
            self.__action.notify_all()

    @contextmanager
    def paused(self):
        '''
        Context Manager that pauses the thread then resumes it
        '''
        yield self.pause()
        self.resume()

    #########################################
    # Internal Methods

    def pause_point(self):
        '''
        Used to indicate a potential stopping point for the thread.
        Sees if someone wants this thread to pause, and sleeps until
        resumes if this is so
        '''
        with self.__action:
            # Check if someone wants us to pause
            if not self.__pause_request:
                return

            # Ensure we turn off the pause request
            self.__pause_request = False

            # Wake the parent, then wait for it
            self.__action.notify_all()
            self.__action.wait()


