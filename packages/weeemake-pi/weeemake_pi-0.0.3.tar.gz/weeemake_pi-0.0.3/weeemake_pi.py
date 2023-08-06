# -*- coding: utf-8 -*

import sys

if sys.version > '3':
    PY3 = True
    print("\r\nVersion:" + sys.version)
    from weeemake_pi_python3 import *
else:
    PY3 = False
    print("\r\nVersion:" + sys.version)
    from weeemake_pi_python2 import *