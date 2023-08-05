"""Entity-relationship classes for the :mod:`v2.db` module.

All model classes define a convenience class-method ``query``, which is in fact a shortcut to calling
:meth:`v2.db.ScopedSession.query` with that class passed as the first argument.
"""

from . import stimulus
from .base import *
from .core import *
from .protocol import *
from .sorting import *
