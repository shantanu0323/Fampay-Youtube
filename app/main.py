from flask import Flask, request, make_response, jsonify
import time
import threading
import app.db_helper as DbHelper
from functools import wraps


SCHEDULER_ACTIVE = False

# Auth enums
AUTH_KEY_INVALID = -1
AUTH_KEY_EXPIRED = 0
AUTH_KEY_VALID = 1

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
    app.config["FAMPAY_KEY"] = "17yEEyXAqeS9JNDpTlBvKLUBr9CfRP1ay4kf"

    SCHEDULER_ACTIVE = False

    def api_required(f) :
        @wraps(f)
        def wrap(*args,**kwargs):
            auth_status = DbHelper.is_api_authentic(app.config["FAMPAY_KEY"])
            message = ""
            if auth_status == AUTH_KEY_EXPIRED:
                message = "API Key has EXPIRED. Restricting access."
            elif auth_status == AUTH_KEY_INVALID:
                message = "API Key is INVALID. Restricting access."
            elif auth_status == AUTH_KEY_VALID:
                message = "API Key is VALID. Allowing access."
            
            return f({
                "message": message,
                "authStatus": auth_status > 0
            }, *args, **kwargs)
        return wrap

    def authenticate():
        auth_status = DbHelper.is_api_authentic(app.config["FAMPAY_KEY"])
        message = ""
        if auth_status == AUTH_KEY_EXPIRED:
            message = "API Key has EXPIRED. Restricting access."
        elif auth_status == AUTH_KEY_INVALID:
            message = "API Key is INVALID. Restricting access."
        elif auth_status == AUTH_KEY_VALID:
            message = "API Key is VALID. Allowing access."
        
        return f({
            "message": message,
            "authStatus": auth_status > 0
        }, *args, **kwargs)

    @app.route("/")
    @api_required
    def index():
        if not auth["authStatus"]:
            return auth["message"]
        global SCHEDULER_ACTIVE
        SCHEDULER_ACTIVE = False
        return "Hello World !!! {0}".format(testing)

    @app.route("/search/")
    @api_required
    def search(auth):
        if not auth["authStatus"]:
            return auth["message"]
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
    @api_required
    def get_videos(auth):
        if not auth["authStatus"]:
            return auth["message"]
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


    @app.route("/search_videos/", methods=["GET"])
    @api_required
    def search_videos(auth):
        if not auth["authStatus"]:
            return auth["message"]
        query = request.args.get('query')
        if query is None:
            return "You got to add the 'query' param to the url"
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
        
        videos, response_msg, total_pages, page_number = DbHelper.search_videos_from_db(query, page_number, max_results)
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


    @app.route("/create_api/", methods=["GET"])
    def create_api():
        api_credentials = DbHelper.create_api_key()
        response = make_response(
            jsonify(api_credentials),
            200,
        )
        return response

    return app

