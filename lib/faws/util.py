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
