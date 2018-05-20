import random

def strfdelta(tdelta, fmt):
    """ timedelta formatter """
    d = {"D": tdelta.days}
    d["h"], rem = divmod(tdelta.seconds, 3600)
    d["m"], d["s"] = divmod(rem, 60)
    return fmt.format(**d)

def RandomColor():
	return int('0x' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]), 0)