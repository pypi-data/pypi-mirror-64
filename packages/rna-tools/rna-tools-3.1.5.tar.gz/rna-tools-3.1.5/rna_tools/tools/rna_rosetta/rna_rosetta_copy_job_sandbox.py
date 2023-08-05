#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage::

  $ rna_rosetta_n.py ade.out
  21594

"""
from subprocess import call

import subprocess
import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help='')
    parser.add_argument('dst', help='')
    return parser

#main
if __name__ == '__main__':
    args = get_parser().parse_args()
    call("cp -rv " + args.src + " " + args.dst, shell=True)
    
