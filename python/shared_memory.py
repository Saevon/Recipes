import multiprocessing
import ctypes


class SharedMemoryString(object):
    '''
    Shared Memory Value that lets you work with a mutable string

    >>> shared_string = SharedMemoryString(
        max_size=1024,
        default='hello',
    )
    >>> with shared_string.get_lock():
    ...     shared_string.set('New Value')
    >>> with shared_string.get_lock():
    ...     shared_string.get() == 'New Value'
    '''

    def __init__(self, max_size, default='', encoding=u'utf-8', lock=True):
        '''
        max_size:     The max_size of the array in bytes. (Immutable)
        default:  Starting value for the string
        encoding: encoding string as accepted by .encode() / .decode()
        '''
        self.max_size = max_size

        self.encoding = encoding

        # The shared data goes here
        if lock is True:
            self._lock = multiprocessing.RLock()
        elif lock is not False:
            self._lock = lock
        else:
            self._lock = None

        self._stored_size = multiprocessing.RawValue(
            ctypes.c_int,
            0,
        )
        self._data = multiprocessing.RawArray(
            ctypes.c_char,
            max_size,
        )

        # For faster access
        self._memory = memoryview(self._data)

        with self._lock:
            self.set(default)

    def __len__(self):
        '''
        Returns the length of the currently stored string.
         * Remember to lock the underlying data if you want consistency
        '''
        return self._stored_size.value

    def __getitem__(self, slice_info):
        '''
        Supports slicing.
         * Remember to lock the underlying data if you want consistency
        '''
        return bytes(
            self._memory
            # First we chop it to the "used" bytes
            [:self._stored_size.value]
            # Then we actually slice on that
            [slice_info]
        ).decode(self.encoding)

    def __setitem__(self, slice_info, value):
        '''
        Supports slice assignment, affects the underlying memory directly.
         * Remember to lock the underlying data if you want consistency

        This will ONLY affect only affect the currently used memory.
          If you wish to write outside of those bounds use .resize() first
        '''
        if isinstance(slice_info, int):
            self._data[slice_info] = value.encode(self.encoding)
            return
        elif slice_info.step is None or slice_info.step >= 0:
            if slice_info.stop is None or slice_info.stop >= self._stored_size.value:
                stop = self._stored_size.value
            elif slice_info.stop < 0:
                stop = max(self._stored_size.value - slice_info.stop, 0)
            else:
                stop = slice_info.stop

            if slice_info.start is None or slice_info.start >= 0:
                start = slice_info.start
            else:
                start = max(self._stored_size.value - slice_info.start, 0)
        else:
            # Reverse slice, our start is the actual stop
            if slice_info.start is None or slice_info.start >= self._stored_size.value:
                start = self._stored_size.value - 1
            elif slice_info.start < 0:
                start = max(self._stored_size.value - slice_info.start, 0)
            else:
                start = slice_info.start

            if slice_info.stop is None or slice_info.stop >= 0:
                stop = slice_info.stop
            else:
                stop = max(self._stored_size.value - slice_info.stop, 0)

        data = value.encode(self.encoding)

        (
            self._data
            # First we chop it to the "used" bytes
            # [:self._stored_size.value]
            # Then we actually slice on that
            [start:stop:slice_info.step]
        ) = data
        # (ctypes.c_char * len(data)).from_buffer(data)

    def __iadd__(self, value):
        '''
        Adds an extra string at the end of the existing one
         * If there isn't enough space, new data gets cut off
        '''
        value = value[:self.max_size - self._stored_size.value]
        data = value.encode(self.encoding)

        self._data[self._stored_size.value:self._stored_size.value + len(data)] = data
        self._stored_size.value = self._stored_size.value + len(data)

        return self

    def resize(self, size=None):
        '''
        Changes the currently used size, without changing the data.
         * Enlarging the size will not reset any trailing bytes
         * Useful for using slice assignment to mess with out-of-bounds data

         * Remember to lock the underlying data if you want consistency

        This cannot change the max_size
        '''
        if size > self.max_size:
            raise ValueError("SharedMemoryString Cannot resize past max-size")
        elif size < 0:
            raise ValueError("SharedMemoryString Cannot resize to a negative size")

        self._stored_size.value = size

    def set(self, value):
        '''
        Copies in a string value, replacing the current data

         * If there isn't enough space, it gets cut off
         * This won't zero out any remaining data
        '''
        value = value[:self.max_size]
        data = value.encode(self.encoding)

        self._data[:len(data)] = data
        self._stored_size.value = len(data)

    def get(self):
        ''' Gets the underlying string value '''
        # Grab just the useful data
        return bytes(self._memory[:self._stored_size.value]).decode(self.encoding)

    def get_lock(self):
        ''' Returns the lock guarding this SharedMemory object '''
        return self._lock


if __name__ == '__main__':
    shared_data = SharedMemoryString(
        max_size=16,
        default='Hello',
        encoding='ascii',
    )

    assert shared_data.get() == 'Hello', "Should respects `default` value"
    assert len(shared_data) == 5, "`default` should set size"

    shared_data.set('1234567890abcdef')
    assert shared_data.get() == '1234567890abcdef', "Should allow full-data use"
    assert len(shared_data) == 16, "Maxing should set size"

    # --------------------------------------------------------------------------
    # +=

    shared_data.set('merge')
    shared_data += ' me'
    assert shared_data.get() == 'merge me', "+= appends data"
    assert len(shared_data) == 8, "appending should update size"

    # --------------------------------------------------------------------------
    # Overflows

    shared_data.set('1234567890abcdefg')
    assert shared_data.get() == '1234567890abcdef', "Should throws out extra data"
    assert len(shared_data) == 16, "Overflows shouldn't mess up the size"

    shared_data += 'other'
    assert shared_data.get() == '1234567890abcdef', "+= should throw out extra data"
    assert len(shared_data) == 16, "Overflows shouldn't mess up the size"

    shared_data.set('1234567890')
    shared_data += '123456789'
    assert shared_data.get() == '1234567890123456', "+= appends as much as it can"
    assert len(shared_data) == 16, "Overflows shouldn't mess up the size"

    over_shared = SharedMemoryString(
        max_size=4,
        default='apple',
        encoding='ascii',
    )
    assert over_shared.get() == 'appl', "default should also check for overflow"
    assert len(over_shared) == 4, "Overflows shouldn't mess up the size"

    # --------------------------------------------------------------------------
    # Resizing

    shared_data.set('wonderfull')
    assert len(shared_data) == 10, "Assigning should change size"

    shared_data.resize(5)
    assert shared_data.get() == 'wonde', "Resizing should lop off data"
    assert len(shared_data) == 5, "Resizing should change length"

    shared_data.resize(7)
    assert shared_data.get() == 'wonderf', "Resizing should bring back data"
    assert len(shared_data) == 7, "Resizing should change length"

    shared_data.set('hello')
    try:
        shared_data.resize(1024)
    except ValueError:
        pass
    else:
        assert False, "Resizing past max-size should raise an error"
    assert len(shared_data) == 5, "bad resizing shouldn't mess with size"

    try:
        shared_data.resize(-1)
    except ValueError:
        pass
    else:
        assert False, "Resizing to negative should raise an error"
    assert len(shared_data) == 5, "bad resizing shouldn't mess with size"

    # --------------------------------------------------------------------------
    # Slicing
    shared_data.set('1234567890abcdef')

    assert shared_data[:] == '1234567890abcdef'
    assert shared_data[:5] == '12345'
    assert shared_data[3:] == '4567890abcdef'
    assert shared_data[:-1] == '1234567890abcde'
    assert shared_data[:-10] == '123456'
    assert shared_data[-12:-10] == '56'
    assert shared_data[-1:-10:-1] == 'fedcba098'
    assert shared_data[3:1:-1] == '43'
    assert shared_data[::-2] == 'fdb08642'

    assert shared_data[::2] == '13579ace'

    # Slicing should respect the current size
    shared_data.set('apple')
    assert shared_data[:] == 'apple'
    assert shared_data[3:] == 'le'
    assert shared_data[3:10000] == 'le'
    assert shared_data[::2] == 'ape'

    assert shared_data[::-1] == 'elppa'
    assert shared_data[:-10:] == ''
    assert shared_data[:-2:] == 'app'
    assert shared_data[-3::] == 'ple'
    assert shared_data[-20:-3:] == 'ap'
    assert shared_data[3:1:-1] == 'lp'

    # Assignment slicing
    shared_data[:] = 'cheer'
    assert shared_data.get() == 'cheer'
    assert len(shared_data) == 5, "assign shouldn't mess with size"

    shared_data[0] = 's'
    assert shared_data.get() == 'sheer'
    assert len(shared_data) == 5, "assign shouldn't mess with size"

    try:
        shared_data[:] = 'overflow'
        shared_data.resize(1024)
    except ValueError:
        pass
    else:
        assert False, "Assigning past the size should error out"
    try:
        shared_data[1:3] = 'a'
        shared_data.resize(1024)
    except ValueError:
        pass
    else:
        assert False, "Assigning not enough characters should error out"

    shared_data[:2:-1] = 'aa'
    assert shared_data.get() == 'sheaa'

    shared_data[:2:] = 'aa'
    assert shared_data.get() == 'aaeaa'

    shared_data[::-1] = 'elppa'
    assert shared_data.get() == 'apple'

    shared_data[::-2] = '___'
    assert shared_data.get() == '_p_l_'
    shared_data[1::2] = '..'
    assert shared_data.get() == '_._._'

    shared_data.resize(16)
    assert shared_data.get() == '_._._67890abcdef', "Old data shouldn't have been affected"

    shared_data.set('12345')
    shared_data[10] = 'a'
    assert shared_data.get() == '12345', 'You can assign past the array'

    import time

    def _test_async():
        def reader(shared):
            counter = 0

            while True:
                counter += 1
                with shared.get_lock():
                    print(shared[1:])
                    # print(shared.get())

                time.sleep(0.01)

        def writer(shared):
            counter = 0

            while True:
                with shared.get_lock():
                    # shared[6:] = '{:<2}'.format(counter % 100)
                    shared.set('Hello ')
                    shared += '{}'.format(counter % 100)

                counter += 1
                time.sleep(0.01)

        shared_data = SharedMemoryString(
            max_size=1024,
            default='Hello   ',
            encoding='ascii',
        )

        read_process = multiprocessing.Process(
            target=reader,
            kwargs={
                'shared': shared_data,
            },
        )
        read_process.start()

        time.sleep(0.2)

        write_process = multiprocessing.Process(
            target=writer,
            kwargs={
                'shared': shared_data,
            },
        )
        write_process.start()

        read_process.join()
        write_process.join()
