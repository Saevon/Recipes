#!/usr/bin/python
import bottle
import json
import os
import re

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

def if_upload_enabled(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        path = app.config['upload_path']
        if path is False:
            raise bottle.HTTPError(status=404)
        kwargs['upload_path'] = path

        return func(*args, **kwargs)
    return wrapper



@app.route('/upload', method='GET')
@if_upload_enabled
def upload_html(upload_path):
    output = u''

    success = 'success' in bottle.request.params
    if success:
        output += u'''
            Upload Succeded<script type="text/javascript">history.pushState({}, "Upload", "/upload");</script>
        '''

    output += u'''
        <form action="/upload" method="post" enctype="multipart/form-data">
            Select a file: <input type="file" name="upload" />
            <input type="submit" value="Start upload" />
        </form>
    '''

    return output

COPY_RE = re.compile(r'^(?P<name>.*) \((?P<num>[0-9]+)\)$')

@app.route('/upload', method='POST')
@if_upload_enabled
def upload(upload_path):
    upload = bottle.request.files.get('upload')

    name, ext = os.path.splitext(upload.filename)
    # if ext not in ('png', 'jpg', 'jpeg'):
    #     return 'File extension not allowed.'

    while os.path.exists(os.path.join(upload_path, name + ext)):
        match = COPY_RE.match(name)
        if match is not None:
            name = match.group('name')
            num = int(match.group('num'))
        else:
            num = 1
        name = '%s (%i)' % (name, num)

    full_path = os.path.join(upload_path, name + ext)
    upload.save(full_path)

    print "Uploaded: %s" % full_path

    bottle.redirect('/upload?success')

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
    'static_root': 'static',
    'upload_path': False,

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
    "--upload",
    dest="upload_path",
    action="store",
    help="THe folder to save uploaded files (uploading is disabled unless this option is passed in",
)
app_parser.add_option(
    "-q", "--quiet",
    dest="debug",
    action="store_false",
)
app_parser.add_option(
    "--host",
    dest="host",
    action="store",
)
app_parser.add_option(
    "--open",
    dest="host",
    action="store_const",
    const="0.0.0.0",
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
    elif options.host:
        app.config['host'] = options.host

    # Check that the root path is valid
    if options.static_root and not os.path.exists(options.static_root):
        app_parser.error("Root path does not exist: %" % options.static_root)

    # Remove any unset options, using the defaults defined earlier instead
    options = vars(options)
    options = dict((key, options[key]) for key in options if options[key] is not None)

    return options


if __name__ == '__main__':
    options = parse_options()

    app.config.update(options)

    # Debug only settings go here
    if app.config["debug"]:
        bottle.debug(True)
        app.config.update({
            'reloader': True,
            'quiet': False,
        })

    app.run(**app.config)
