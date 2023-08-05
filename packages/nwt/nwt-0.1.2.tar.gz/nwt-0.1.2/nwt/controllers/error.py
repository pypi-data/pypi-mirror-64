#! -*- coding: utf-8 -*-
"""
nwt.controllers.error
---------------------

Handle all possible error in nwt.
"""

import sys
from functools import wraps

from logzero import logger as log
from requests.exceptions import ConnectionError


class NwtError(Exception):
	"""
	Base class for Nwt errors.

	This is the base class for "nice" exceptions. When such an exception is
	raised. Nwt will abort the build and present the exception category and
	message to the user.

	Extensions are encouraged to derive from this exception for their custom
	errors.

	.. attribute:: category

	   Description of the exception "category", used in converting the
	   exception to a string ("category: message").  Should be set accordingly
	   in subclasses.
	"""
	category = 'Nwt error'


class NwtWarning(NwtError):
	"""
	Warning, treated as error.
	"""
	category = 'Nwt error'


class ConfigError(NwtError):
	"""
	Configuration error.
	"""
	category = 'Configuration error'


class InputError(NwtError):
	"""
	User input error.
	"""
	category = 'Input error'


def error_handler(func):
	@wraps(func)
	def warped(*args, **kwargs):
		try:
			return func(*args, **kwargs)

		except NwtError as e:
			log.error(e)
			sys.exit(3)

		except ModuleNotFoundError as e:
			log.error(f'Module not found error: Please install "{e.name}"')
			sys.exit(2)

		except ConnectionError as e:
			log.error('No internet connection')
			sys.exit(1)

	return warped
