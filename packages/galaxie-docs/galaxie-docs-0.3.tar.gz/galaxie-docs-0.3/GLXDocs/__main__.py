import argparse
import os
from GLXDocs import Docs

__authors__ = ["Tuxa"]
__date__ = 20200325
__version__ = 0.3
__description__ = "Galaxie Docs"


def md2html():
    docs = Docs()
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by Galaxie under GPLv3+ license"
    )
    parser.add_argument("source", help="source file path")
    parser.add_argument("destination", help="destination file path")
    parser.add_argument('--lang',
                        dest='lang',
                        default='en',
                        help="HTTP_ACCEPT_LANGUAGE"
                        )

    parser.add_argument('--charset',
                        dest='charset',
                        default='utf-8',
                        help="character sets"
                        )
    args = parser.parse_args()
    docs.lang = args.lang
    docs.charset = args.charset
    if os.sep in args.source:
        docs.add_src_file_name(args.source.split(os.sep, 1)[1])
    else:
        docs.add_src_file_name(args.source)

    docs.add_dst_file_name(os.path.abspath(args.dest))
    docs.md2html()
