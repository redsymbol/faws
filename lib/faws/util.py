def random_name(prefix=None):
    import time
    from random import randint
    from sys import maxsize
    prefix = prefix or 'AMI'
    return '{}-{}-{}'.format(
        prefix,
        int(time.time()),
        randint(maxsize >> 3, maxsize),
        )

def assert_pyversion():
    import sys
    assert sys.version_info.major >= 3, sys.version
    assert sys.version_info.minor >= 3, sys.version
