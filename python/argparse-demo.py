# Full Argparse example
import argparse
import logging


# Values for the -v, each `v` means it goes up a level
# Comment out some to skip stages
# The first one is for 'no -v'
VERBOSITY = [
    # logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL,
]


def parse(raw_args=None):
    ''' CLI command parser '''

    # --------------------------------------------------------------------------
    # Shared arguments
    shared_args = argparse.ArgumentParser(add_help=False)

    shared_args.add_argument(
        '-v', '--verbose',
        dest='verbose', action='count', default=0,
        help='Increases verbosity',
    )

    # --------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description='Process some integers.',
        parents=[shared_args],
    )

    # You can now read the "args.command" to see which one was chosen
    subparsers = parser.add_subparsers(title='commands', dest='command')
    subparsers.required = True

    # --------------------------------------------------------------------------
    # A list command
    list_parser = subparsers.add_parser('list', parents=[shared_args], help='List contents')
    list_parser.add_argument('dirname', action='store', help='Directory to list')

    # --------------------------------------------------------------------------
    # A create command
    create_parser = subparsers.add_parser('create', parents=[shared_args], help='Create a directory')
    create_parser.add_argument('dirname', action='store', help='New directory to create')

    # --------------------------------------------------------------------------
    # A delete command
    delete_parser = subparsers.add_parser('delete', parents=[shared_args], help='Remove a directory')
    delete_parser.add_argument('dirname', action='store', help='The directory to remove')

    args = parser.parse_args(raw_args)

    # --------------------------------------------------------------------------
    # Validation & Post-processing
    if args.verbose >= len(VERBOSITY):
        raise parser.error('Too verbose: {}'.format(args.verbose))
    args.verbose = VERBOSITY[args.verbose]

    return args

    # You can now read `args.command` to see which subcommand was chosen



# -------------------------------------------------------------------------------
# Alternate flag styles

parser = argparse.ArgumentParser(
    description='Process some integers.',

    # lets you change which characters act as prefixes for long options
    # Windows Style:
    # /option
    # You then need to list every version in the "add_argument"
    # BUT! they can do different things
    prefix_chars='-+/',
)

# Common Version Arg
parser.add_argument('-v', '--version', action='version', version='%(prog)s ')# #__version__)

# TODO: Create a 'environment_default' argparser?
#    * It grabs in order of priority:
#      1. commandline args
#      2. environment variables
#      3. .env variables
#      4. defaults specified by argparse
#    * It also adds this to the help text (showing each variable/flag/default)


###########################
# + - to toggle things (remember to enable prefix_chars)
parser.add_argument(
    '-a', '--apples',
    dest="var_a", action="store_false",
)

parser.add_argument(
    '+a', '++apples',
    dest="var_a", action="store_true",
)


############################
# Sample arguments


# nargs:
#    int
#    ?    0 or 1
parser.add_argument('--mode', nargs='?', const='if no value is passed')
#    *    0 to all
#    +    1 to all
#    argparse.REMAINDER  collects unused args

parser.add_argument('--mode', choices=('read-only', 'read-write'))

# Actually opens the file
parser.add_argument('-i', metavar="infile", type=argparse.FileType('rt'))
parser.add_argument('-o', metavar="outfile", type=argparse.FileType('wt'))


parser.add_argument(
    'file',
    type=str, nargs=1,
    metavar='icon-file', help='file to read/write icon to',
)

parser.add_argument(
    '-e', '--export',
    dest='action', action='store_const',
    const='export',
    help='Exports the file',
)
parser.add_argument(
    '-e', '--export',
    dest='action', action='store_const',
    const='export',
    help='Exports the file',
)
parser.add_argument(
    '-w', '--write',
    dest='action', action='store',
    metavar='act', help='Writes the given icon to the file/folder',
)


########################
# Working with lists
parser.add_argument(
    '-a', '--append',
    action='append', dest='collection', default=[],
    metavar='item', help='Add repeated values to a list',
)

parser.add_argument(
    '-B',
    action='append_const', dest='const_collection', const='Value-B',
    default=[],
    metavar='item', help='Add different values to list',
)
parser.add_argument(
    '-C',
    action='append_const', dest='const_collection', const='Value-C',
    metavar='item', help='Add different values to list',
)

# TODO: Create a 'chain_list' action
#    * for using 'append' with nargs=2+
#    * with alternative for using const if "nargs=0"


###########################
# Reusing Parsers (Parents)
os_parser = argparse.ArgumentParser(add_help=False)

group1 = os_parser.add_argument_group('osDetection')
group1.add_argument('--windows', action='store_true')
group1.add_argument('--linux', action='store_true')
group1.add_argument('--mac', action='store_true')

# Now other parsers can reuse this
script1_parser = argparse.ArgumentParser(parents=[os_parser])
script2_parser = argparse.ArgumentParser(parents=[os_parser])
script3_parser = argparse.ArgumentParser(parents=[os_parser])






####################
# Argument groups
parser = argparse.ArgumentParser(add_help=False)

group1 = parser.add_argument_group('authentication')
group1.add_argument("...")

# Mutually exclusive groups
group = parser.add_mutually_exclusive_group('authentication')
group.add_argument('-u', '--user', action='store_true')
group.add_argument('-t', '--token', action='store_true')




args = parser.parse_args()



# ---------------------------------
# Errors
raise parser.error('Invalid thing: {}'.format(args.argument_name))


def arg_real_path(path):
    ''' Ensures this is a vlaid existing folder '''

    # Validate
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError('Invalid path: {}'.format(path))

    # Convert
    return os.path.abspath(path)


# Default does not pass through the type() conversion
parser.add_argument('--output-dir', action='store', type=arg_real_path, default=None)








