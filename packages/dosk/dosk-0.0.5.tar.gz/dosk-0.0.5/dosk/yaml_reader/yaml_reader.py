#!/usr/bin/env python

from pathlib import Path
import yaml

def test():
    # do the real work:
    print("Capitalizing: on poopy butthole")

    document = """
  a: 1
  b:
    c: 3
    d: 4
"""
    print (yaml.dump(yaml.load(document)))