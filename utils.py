"""
Utility functions to make the smsweb code easier to read.
"""

from __future__ import print_function
from os import getenv
import sys

def env_var(name):
    """
    Look up an env var by name.
    If the env var is not defined, print a standard message to STDERR and exit.
    """
    value = getenv(name, None)
    if value is None:
        print("You must set the environment variable", name, file=sys.stderr)
        sys.exit(1)

    return value

def extract_error(response):
    """
    Extract the first error message in a send_message response dict.
    Returns the error text if an error is found, otherwise None.
    """
    for responses in response['messages']:
        if responses['status'] != '0':
            return responses['error-text']