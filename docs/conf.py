import os
import sys

from recommonmark.parser import CommonMarkParser

sys.path.insert(0, os.path.abspath('..'))

source_parsers = {
    ".md": CommonMarkParser,
}

source_suffix = [".rst", ".md"]

extensions = ["sphinx.ext.autodoc", "sphinxcontrib.napoleon"]
