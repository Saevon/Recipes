from flask import Flask
from werkzeug.routing import BaseConverter



class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]




app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter





# To get all URLs ending with "/number"
@app.route("/<regex('.*/([0-9]+)'):param>/")
def go_to_one(param):
    return param.split("/")[-1]
