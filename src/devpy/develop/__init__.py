import sys

from devpy import dev_mode


sys.modules['devpy.develop'] = dev_mode()
