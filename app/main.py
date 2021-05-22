from flask import Flask, request
import time
import threading

from flask.wrappers import Request

SCHEDULER_ACTIVE = False

def synchronise():
    global SCHEDULER_ACTIVE
    print("*" * 40)
    print("Task execution started...")
    print(SCHEDULER_ACTIVE)
    time.sleep(4)
    print("Task execution completed.")
    if (SCHEDULER_ACTIVE):
        synchronise()
    return


def create_app(testing : bool =  True):
    global SCHEDULER_ACTIVE
    app = Flask(__name__)
    SCHEDULER_ACTIVE = False

    @app.route("/")
    def index():
        global SCHEDULER_ACTIVE
        SCHEDULER_ACTIVE = False
        return "Hello World !!! {0}".format(testing)

    @app.route("/search/")
    def search():
        global SCHEDULER_ACTIVE
        query = request.args.get("query")
        print(query)
        SCHEDULER_ACTIVE = True
        threading.Thread(target=synchronise).start()
        return "Synchronising..."

    return app

