"""A global Jinja2 Environment instance used by gmxbatch at various places"""

import jinja2

jinjaenv = jinja2.Environment(loader=jinja2.PackageLoader('gmxbatch', 'resource'),
                              trim_blocks=False, lstrip_blocks=False, keep_trailing_newline=False)
