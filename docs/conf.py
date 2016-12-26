from sphinx.apidoc import main

from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']
main(["-e", "-o", "developer", "../cactusbot"])
