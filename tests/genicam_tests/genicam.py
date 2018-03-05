"""
Legacy support module enabling the user to "import genicam"

This module simply re-imports from pypylon.genicam...
"""

from warnings import warn

warn("importing from 'genicam' is deprecated. Import from 'pypylon.genicam' instead.", DeprecationWarning)

from pypylon.genicam import *
