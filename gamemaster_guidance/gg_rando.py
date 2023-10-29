import random


def rand_percent():
    """Return an integer between 1 and 100"""
    return int(100 * random.uniform(0.01, 1.0))


def rand_integer(min, max):
	"""Return an integer min <= n <= max"""
	# LOCAL VARIABLES
	retInt = None
	localMin = min
	localMax = max

	# INPUT VALIDATION
	if not isinstance(min, int):
		raise TypeError("min is not an integer")
	elif not isinstance(max, int):
		raise TypeError("max is not an integer")
	# Wrong order
	elif min > max:
		localMin = max
		localMax = min

	# RANDO
	try:
		retInt = random.randint(localMin, localMax)
	except Exception as err:
		print(repr(err))
		raise err

	# DONE
	return retInt


def rand_float(start, stop):
    """Return a random float between start and stop"""
    return random.uniform(start, stop)
