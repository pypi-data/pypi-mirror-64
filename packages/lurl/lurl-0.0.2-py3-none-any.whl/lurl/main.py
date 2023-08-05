from optparse import OptionParser
import sys
from . import tkp_struct, args_parser

def main():
    parser, options, arguments = args_parser.parse_options()
    
    if not options.curl_prod is None or not options.curl_stag is None:
        req = tkp_struct.TkpStruct(options.curl_prod,options.curl_stag)
        req.get_as_tkp()

    sys.exit(0)

if __name__ == '__main__':
    main()