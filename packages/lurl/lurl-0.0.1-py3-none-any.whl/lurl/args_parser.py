from optparse import OptionParser
import sys

def parse_options():
    """
    Handle command-line options with optparse.OptionParser.

    Return list of arguments, largely for use in `parse_arguments`.
    """

    # Initialize
    parser = OptionParser(usage="lurl [options]")

    parser.add_option(
        '-c','--curl',
        dest='curl',
        default=None,
        help="put your cURL"
    )

    # Finalize
    # Return three-tuple of parser + the output from parse_args (opt obj, args)
    opts, args = parser.parse_args()
    return parser, opts, args