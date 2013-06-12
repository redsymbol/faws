from concurrent.futures import Future as StdFuture
from .result import AWSResult

class Future(StdFuture):
    def __init__(self, std_future : 'concurrent.futures.Future'):
        self.std_future = std_future
        
    def result(self, *a, **kw):
        response = super().result(*a, **kw)
        return AWSResult(response.text)

    def __getattr__(self, name):
        # Fall back to self.std_future object where we can
        if hasattr(self.std_future, name):
            return getattr(self.std_future, name)
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))
