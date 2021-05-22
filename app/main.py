from flask import Flask, request
import time
import threading
import app.db_helper as DbHelper

SCHEDULER_ACTIVE = False

def synchronise(url, query, api_key, published_after, max_results):
    global SCHEDULER_ACTIVE
    print("*" * 40)
    print("Task execution started...")
    print(SCHEDULER_ACTIVE)
    DbHelper.sync_db_with_yt(url, query, api_key, published_after, max_results)
    time.sleep(10)
    print("Task execution completed.")
    if (SCHEDULER_ACTIVE):
        synchronise(url, query, api_key, published_after, max_results)
    return


def create_app(testing : bool =  True):
    global SCHEDULER_ACTIVE
    app = Flask(__name__)

    app.config["YOUTUBE_API_KEY"] = "AIzaSyC4jvBZgNGWjtwvjsGNKcbrZ1ddS82K8BY"
    app.config["PUBLISHED_AFTER"] = "2021-05-22T00:00:00Z"
    app.config["MAX_RESULTS"] = 50
    app.config["YOUTUBE_URL"] = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&order=date&key={api_key}&q={query}&publishedAfter={published_after}&maxResults={max_results}"

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
        threading.Thread(target=synchronise, args=(
            app.config["YOUTUBE_URL"],
            query, 
            app.config["YOUTUBE_API_KEY"], 
            app.config["PUBLISHED_AFTER"], 
            app.config["MAX_RESULTS"]
        )).start()
        return "Synchronising..."

    return app

