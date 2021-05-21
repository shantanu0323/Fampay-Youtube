from flask import Flask

def create_app(testing : bool =  True):
    app = Flask(__name__)
    
    @app.route("/")
    def index():
        return "Hello World Wsup!!! {0}".format(testing)

    return app