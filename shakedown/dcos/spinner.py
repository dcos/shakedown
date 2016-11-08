import time as time_module


def wait_for(predicate, timeout_seconds=120, sleep_seconds=1, ignore_exceptions=True, inverse_predicate=False):
    """ waits or spins for a predicate.  Predicate is in function that returns a True or False.
        An exception in the function will be returned.
        A timeout will throw a TimeoutExpired Exception.

    """

    timeout = Deadline.create_deadline(timeout_seconds)
    while True:
        try:
            result = predicate()
        except Exception as e:
            if not ignore_exceptions:
                raise e
        else:
            if (not inverse_predicate and result) or (inverse_predicate and not result):
                return
            if timeout.is_expired():
                raise TimeoutExpired(timeout_seconds, str(predicate))
        time_module.sleep(sleep_seconds)


def time_wait(predicate, timeout_seconds=120, sleep_seconds=1, ignore_exceptions=True, inverse_predicate=False):
    """ waits or spins for a predicate and returns the time of the wait.
        An exception in the function will be returned.
        A timeout will throw a TimeoutExpired Exception.

    """
    start = time_module.time()
    wait_for(predicate, timeout_seconds, sleep_seconds, ignore_exceptions, inverse_predicate)
    return elapse_time(start)


def elapse_time(start, end=None, precision=3):
    """ Simple time calculation utility.   Given a start time, it will provide an elapse time.
    """
    if end is None:
        end = time_module.time()
    return round(end-start, precision)


class Deadline(object):

    def is_expired(self):
        raise NotImplementedError()

    @staticmethod
    def create_deadline(seconds):
        if seconds is None:
            return Forever()
        return Within(seconds)


class Within(Deadline):

    def __init__(self, seconds):
        super(Within, self).__init__()
        self._deadline = time_module.time() + seconds

    def is_expired(self):
        return time_module.time() >= self._deadline


class Forever(Deadline):

    def is_expired(self):
        return False


class TimeoutExpired(Exception):
    def __init__(self, timeout_seconds, what):
        super(TimeoutExpired, self).__init__(timeout_seconds, what)
        self._timeout_seconds = timeout_seconds
        self._what = what

    def __str__(self):
        return "Timeout of {0} seconds expired waiting for {1}".format(self._timeout_seconds, self._what)

    def __repr__(self):
        return "{0}: {1}".format(type(self).__name__, self)

    def __unicode__(self):
        return u"Timeout of {0} seconds expired waiting for {1}".format(self._timeout_seconds, self._what)
