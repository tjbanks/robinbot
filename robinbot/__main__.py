import argparse
from argparse import RawTextHelpFormatter,SUPPRESS
import sys

use_description = """
A Robinhood crypto trading bot powered by machine learning.
"""

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=use_description, formatter_class=RawTextHelpFormatter,usage=SUPPRESS)
    options = None
    try:
        if not len(sys.argv) > 1:
            raise
        if sys.argv[1] in ['-h','--h','-help','--help','help']:
            raise
        options = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)