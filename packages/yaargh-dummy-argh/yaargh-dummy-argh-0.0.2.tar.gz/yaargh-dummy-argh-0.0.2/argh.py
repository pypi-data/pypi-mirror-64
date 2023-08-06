
"""
This is a dummy module. When imported, it replaces itself (and submodules) with yaargh.

The intent is to allow unmodified programs to "import argh",
but actually be using yaargh.
"""

import yaargh

import sys

# We need to also add all submodules of yaargh to sys.modules,
# otherwise when we import argh.foo it will create a new instance of yaargh.foo,
# causing much confusion.
# Our method here is not perfect - any modules that are not imported by "import yaargh"
# won't be found. But as of writing, there are no modules like that.

# Find all imported submodules of yaargh.
# Take copy of keys because we're modifying sys.modules mid-loop
for module_name in list(sys.modules.keys()):
    name_parts = module_name.split('.', 1)
    if len(name_parts) > 1 and name_parts[0] == 'yaargh':
        new_name = '{}.{}'.format(__name__, name_parts[1])
        sys.modules[new_name] = sys.modules[module_name]

# This step must be done last, because afterwards our module is no longer referenced
# and weird things happen (like sys becoming None).
sys.modules[__name__] = yaargh
