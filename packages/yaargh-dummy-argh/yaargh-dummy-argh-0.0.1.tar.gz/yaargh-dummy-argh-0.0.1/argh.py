
"""
This is a dummy module. When imported, it replaces itself with yaargh.

The intent is to allow unmodified programs to "import argh",
but actually be using yaargh.
"""

import yaargh

import sys
sys.modules[__name__] = yaargh
