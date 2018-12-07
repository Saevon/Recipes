# Full Argparse example
import argparse

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

parser.add_argument('-i', metavar='in-file', type=argparse.filetype('rt'))
parser.add_argument('-o', metavar='out-file', type=argparse.FileType('wt'))


parser.add_argument(
    'file',
    metavar='file', type=str, nargs='1',
    help='file to read/write icon to',
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
    help='Writes the given icon to the file/folder',
)


########################
# Working with lists
parser.add_argument(
    '-a', '--append',
    action='append', dest='collection', default=[],
    help='Add repeated values to a list',
)

parser.add_argument(
    '-B',
    action='append_const', dest='const_collection', const='Value-B',
    default=[],
    help='Add different values to list',
)
parser.add_argument(
    '-C',
    action='append_const', dest='const_collection', const='Value-C',
    help='Add different values to list',
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



####################
# Sub parsers
#    like git rm, add, push, etc
parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='commands')

# A list command
list_parser = subparsers.add_parser('list', help='List contents')
list_parser.add_argument('dirname', action='store', help='Directory to list')

# A create command
create_parser = subparsers.add_parser('create', help='Create a directory')
create_parser.add_argument('dirname', action='store', help='New directory to create')

# A delete command
delete_parser = subparsers.add_parser('delete', help='Remove a directory')
delete_parser.add_argument('dirname', action='store', help='The directory to remove')



args = parser.parse_args()

# This also ties in a function, by adding an automatic arg to each command
# (Optional) you probably want to list this above with each argument?
list_parser.set_defaults(func=your_list_func)
create_parser.set_defaults(func=your_create_func)
delete_parser.set_defaults(func=your_delete_func)
args.func(args)

