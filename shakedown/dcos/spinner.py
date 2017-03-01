from dcos import util
import time as time_module
import traceback

import shakedown

from inspect import currentframe, getargvalues, getsource, getouterframes

logger = util.get_logger(__name__)


def wait_for(
        predicate,
        timeout_seconds=120,
        sleep_seconds=1,
        ignore_exceptions=True,
        inverse_predicate=False,
        noisy=False):
    """ waits or spins for a predicate, returning the result.
        Predicate is a function that returns a truthy or falsy value.
        An exception in the function will be returned.
        A timeout will throw a TimeoutExpired Exception.

    """

    start_time = time_module.time()
    timeout = Deadline.create_deadline(timeout_seconds)
    while True:
        try:
            result = predicate()
        except Exception as e:
            if ignore_exceptions:
                if noisy:
                    logger.exception("Ignoring error during wait.")
            else:
                raise  # preserve original stack
        else:
            if (not inverse_predicate and result) or (inverse_predicate and not result):
                return result
            if timeout.is_expired():
                funname = __stringify_predicate(predicate)
                raise TimeoutExpired(timeout_seconds, funname)
        if noisy:
            print('{}[{}/{}] spinning...'.format(
                shakedown.cli.helpers.fchr('>>'),
                pretty_duration(time_module.time() - start_time),
                pretty_duration(timeout_seconds)))
        time_module.sleep(sleep_seconds)


def __stringify_predicate(predicate):
    """ Reflection of function name and parameters of the predicate being used.
    """
    funname = getsource(predicate).strip().split(' ')[2].rstrip(',')
    params = 'None'

    # if args dig in the stack
    if '()' not in funname:
        stack = getouterframes(currentframe())
        for frame in range(0, len(stack)):
            if funname in str(stack[frame]):
                _, _, _, params = getargvalues(stack[frame][0])

    return "function: {} params: {}".format(funname, params)


def time_wait(predicate, timeout_seconds=120, sleep_seconds=1, ignore_exceptions=True, inverse_predicate=False, noisy=True):
    """ waits or spins for a predicate and returns the time of the wait.
        An exception in the function will be returned.
        A timeout will throw a TimeoutExpired Exception.

    """
    start = time_module.time()
    wait_for(predicate, timeout_seconds, sleep_seconds, ignore_exceptions, inverse_predicate, noisy)
    return elapse_time(start)


def elapse_time(start, end=None, precision=3):
    """ Simple time calculation utility.   Given a start time, it will provide an elapse time.
    """
    if end is None:
        end = time_module.time()
    return round(end-start, precision)


def pretty_duration(seconds):
    """ Returns a user-friendly representation of the provided duration in seconds.
    For example: 62.8 => "1m2.8s", or 129837.8 => "2d12h4m57.8s"
    """
    ret = ''
    if seconds >= 86400:
        ret += '{:.0f}d'.format(int(seconds / 86400))
        seconds = seconds % 86400
    if seconds >= 3600:
        ret += '{:.0f}h'.format(int(seconds / 3600))
        seconds = seconds % 3600
    if seconds >= 60:
        ret += '{:.0f}m'.format(int(seconds / 60))
        seconds = seconds % 60
    if seconds > 0:
        ret += '{:.1f}s'.format(seconds)
    return ret


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
        return "Timeout of {0} expired waiting for {1}".format(pretty_duration(self._timeout_seconds), self._what)

    def __repr__(self):
        return "{0}: {1}".format(type(self).__name__, self)

    def __unicode__(self):
        return u"Timeout of {0} expired waiting for {1}".format(pretty_duration(self._timeout_seconds), self._what)
