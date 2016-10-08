"""Debug module"""
#!/usr/bin/python3

import time

def time_counter(func):
    """time counter"""
    def inner(*args, **kwargs):
        """This is just inner function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        spended_time = time.time() - start_time
        print("%s runtime: %s" %
              (func.__name__,
               round(spended_time, 4)))
        return result
    return inner
