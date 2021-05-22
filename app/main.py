from flask import Flask, request, make_response, jsonify
import time
import threading
import app.db_helper as DbHelper

SCHEDULER_ACTIVE = False

def synchronise(url, query, api_key, published_after, max_results):
    global SCHEDULER_ACTIVE
    print("*" * 40)
    print("Task execution started...")
    print(SCHEDULER_ACTIVE)
    threading.Thread(target=DbHelper.sync_db_with_yt, args=(url, query, api_key, published_after, max_results)).start()
    # DbHelper.sync_db_with_yt(url, query, api_key, published_after, max_results)
    time.sleep(10)
    print("Task execution completed.")
    if (SCHEDULER_ACTIVE):
        synchronise(url, query, api_key, published_after, max_results)
    return


def create_app(testing : bool =  True):
    global SCHEDULER_ACTIVE
    app = Flask(__name__)
    app.debug = True

    app.config["YOUTUBE_API_KEY"] = "AIzaSyC4jvBZgNGWjtwvjsGNKcbrZ1ddS82K8BY"
    app.config["PUBLISHED_AFTER"] = "2021-05-22T10:00:00Z"
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


    @app.route("/get/", methods=["GET"])
    def get_videos():
        page_number = request.args.get("pageNumber")
        max_results = request.args.get("maxResults")
        if page_number is None:
            page_number = 1
        else:
            page_number = int(page_number)
        if max_results is None:
            max_results = 10
        else:
            max_results = int(max_results)

        videos, response_msg, total_pages, page_number = DbHelper.get_videos_from_db(page_number, max_results)
        response = make_response(
            jsonify({
                "videos": videos,
                "noOfVideos": len(videos),
                "response": response_msg,
                "totalPages": total_pages,
                "pageNumber": page_number
            }),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response
    
    return app

