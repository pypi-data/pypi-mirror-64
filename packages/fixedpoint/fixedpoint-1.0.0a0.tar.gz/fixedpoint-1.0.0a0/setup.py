#!/usr/bin/env python3
from setuptools import setup
from setuptools.config import read_configuration
from pathlib import Path
import re

def long_description():
    """Removes links from long_description.rst"""
    with open(Path(__file__).parent/'docs'/'source'/'long_description.rst') as f:
        rst = f.read()
    def repl(m):
        M = m.group(1)
        return M.split('.')[-1] if M.startswith('~') else M
    desc = re.sub(r':[^:]+:`([^`]+)`', repl, re.sub(r' <[^>]+>', '', rst))
    with open(Path(__file__).parent/'LICENSE') as f:
        license = f.read()
    return f"{desc}\n\n{license}"

cfg = read_configuration(Path(__file__).parent / 'setup.cfg')

cfg['metadata']['long_description'] = long_description()

setup(**cfg['metadata'], **cfg['options'])
