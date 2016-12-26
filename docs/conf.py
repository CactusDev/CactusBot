import os
import sys

from sphinx.apidoc import main

from recommonmark.parser import CommonMarkParser

sys.path.insert(0, os.path.abspath('.'))

source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']
main(["-e", "-o", "developer", "../cactusbot"])
