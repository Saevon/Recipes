#!/usr/bin/python
import bottle


app = bottle.Bottle()


@app.route('/<filename:path>')
def hive_js(filename):
    '''
    Allows access to any file in the static directory
    '''
    return bottle.static_file(filename, root="static")


##################################################
# Settings & Stratup
##################################################
app_settings = {
    'debug': True,

    'host': 'localhost',
    'port': 7070,

    'quiet': True,
}


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
        app_settings['host'] = args[0]

    # Remove any unset options, using the defaults defined earlier instead
    options = vars(options)
    options = dict((key, options[key]) for key in options if options[key] is not None)

    return options


if __name__ == '__main__':
    app_settings.update(parse_options())

    # Debug only settings go here
    if app_settings["debug"]:
        bottle.debug(True)
        app_settings.update({
            'reloader': True,
            'quiet': False,
        })

    app.run(**app_settings)
