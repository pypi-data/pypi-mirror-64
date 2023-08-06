import argparse
import os
from GLXDocs import Docs

__authors__ = ["Tuxa", "Alias la Tuxette"]
__date__ = 20200325
__description__ = "Galaxie Docs"


def md2html():
    docs = Docs()
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument("source", help="Source file")
    parser.add_argument("dest", help="Destination directory or file")

    args = parser.parse_args()

    source = os.path.abspath(args.source)
    if os.sep in args.source:
        docs.add_src_file_name(args.source.split(os.sep, 1)[1])
    else:
        docs.add_src_file_name(args.source)

    docs.add_dst_file_name(os.path.abspath(args.dest))
    docs.md2html()

