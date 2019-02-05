import sys
import os

sys.path.insert(0, os.path.abspath('.'))

import rail

master_doc = 'README'

extensions = [
    'sphinx.ext.autodoc',
]

autodoc_mock_imports = ["rail"]
