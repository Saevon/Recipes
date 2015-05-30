#!/usr/bin/python
import bottle
import json
import os

from functools import wraps


app = bottle.Bottle()


def json_return(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = json.dumps(func(*args, **kwargs), **app.config['json'])
        data = data.replace(' ', '&nbsp;').replace('\n', '<br/>')
        return data

    return wrapper

def list_return(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        return '<br/>'.join(data)
    return wrapper

def is_subdir(path, directory):
    """
    Returns true if *path* in a subdirectory of *directory*.
    """
    path = os.path.realpath(path)
    directory = os.path.realpath(directory)

    return path.startswith(directory)


@list_return
def show_contents(folder):
    # Security: remove any symbolic links
    if not is_subdir(folder, app.config['static_root']):
        raise bottle.HTTPError(status=404)

    print "Showing: ", folder
    files = os.listdir(folder)

    for ext in app.config['folder']['ignore']:
        files = filter(lambda file: not file.endswith(ext), files)

    return sorted(files)


@app.route('/')
def root():
    '''
    Shows the data in the root folder
    '''
    return show_contents(app.config['static_root'])

@app.route('/<filename:path>')
def static(filename):
    '''
    Allows access to any file in the static directory
    '''
    path = os.path.join(app.config['static_root'], filename)
    if not os.path.exists(path):
        raise bottle.HTTPError(status=404)
    if os.path.isdir(path):
        return show_contents(path)

    print "Serving: ", path
    return bottle.static_file(filename, root=app.config['static_root'])


##################################################
# Settings & Startup
##################################################
app.config.update({
    'debug': True,

    'host': 'localhost',
    'port': 7070,

    'quiet': True,

    # Starting static folder
    #'static_root': 'static',
    'static_root': 'folder_list',

    'json': {
        'sort_keys': True,
        'indent': 4,
    },
    'folder': {
        'ignore': [
            '.pyc',
        ],
    }
})


from optparse import OptionParser
app_parser = OptionParser(usage="usage: %prog [host] [options]")
app_parser.add_option(
    "-p", "--port",
    dest="port",
)
app_parser.add_option(
    "-v", "--debug", "--verbose",
    dest="debug",
    action="store_true",
)
app_parser.add_option(
    "-r", "--root",
    dest="static_root",
    action="store",
)
app_parser.add_option(
    "-q", "--quiet",
    dest="debug",
    action="store_false",
)

def parse_options():
    '''
    Reads any commandline options, returning a final dict of options
    '''
    (options, args) = app_parser.parse_args()

    if len(args) > 1:
        app_parser.error("Too many arguments")
    elif len(args) == 1:
        app.config['host'] = args[0]

    # Check that the root path is valid
    if not os.path.exists(options.static_root):
        app_parser.error("Root path does not exist: %" % options['static_root'])

    # Remove any unset options, using the defaults defined earlier instead
    options = vars(options)
    options = dict((key, options[key]) for key in options if options[key] is not None)

    return options


if __name__ == '__main__':
    app.config.update(parse_options())

    # Debug only settings go here
    if app.config["debug"]:
        bottle.debug(True)
        app.config.update({
            'reloader': True,
            'quiet': False,
        })

    app.run(**app.config)
