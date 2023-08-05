#!/usr/bin/env python

"""cli for creating ec2 snapshots"""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import json
import os
import pkg_resources
from stringcolor import cs, bold, underline

def main():
    """cli for creating ec2 snapshots"""
    version = pkg_resources.require("aws-snap")[0].version
    parser = argparse.ArgumentParser(
        description='cli for creating ec2 snapshots',
        prog='aws-snap',
        formatter_class=rawtxt
    )
    parser.add_argument('sgid', nargs="?", help='Security Group ID')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()
    sg_id = args.sgid
    print(sg_id)

if __name__ == "__main__":
    main()
