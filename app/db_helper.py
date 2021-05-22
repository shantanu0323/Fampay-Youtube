# import pymongo
from pymongo import MongoClient, TEXT
from app.models.video import Video
import requests
import json
import math as Math

videosCollection = None


def create_posts(videos : list):
    """
    Create list of dictionaries from Video classes
    :return: List of Dictionaries
    """
    posts = []
    try: 
        for video in videos:
            post = {
                "_id": video.id,
                "title": video.title,
                "description": video.description,
                "publishedAt": video.published_at,
                "thumbnailUrl": video.thumbnail_url
            }
            posts.append(post)
    except Exception as e:
        print("ERROR: Creation of posts from videos failed: {0}".format(e))
        raise e
    return posts


def create_connection(collection_name="Videos"):
    """
    Creating the connection to MongoDB
    :return: None
    """
    global videosCollection
    cluster = None
    try:
        print("Connecting to MongoDB ... ")

        # Earlier method is faster hence going with this
        cluster = MongoClient("mongodb://fampay:fampay@fampay-assignment-shard-00-00.fjsns.mongodb.net:27017,fampay-assignment-shard-00-01.fjsns.mongodb.net:27017,fampay-assignment-shard-00-02.fjsns.mongodb.net:27017/YoutubeStorage?ssl=true&replicaSet=atlas-955f8y-shard-0&authSource=admin&retryWrites=true&w=majority")

        # Newer method is laggy hence avoinding
        # cluster = MongoClient("mongodb+srv://fampay:fampay@fampay-assignment.fjsns.mongodb.net/YoutubeStorage?retryWrites=true&w=majority")
        
        db = cluster["YoutubeStorage"]
        videosCollection = db["Videos"]
        print("Connection Successful.")
    except Exception as e:
        print("CONNECT ERROR: {0}".format(e))
        raise e


def insert_video(video : Video):
    """
    Insert a single video into database
    :return: None
    """
    # Pass the video in a list to the insert_videos() method
    insert_videos([video])


def insert_videos(videos : list):
    """
    Insert videos into the database
    :return: None
    """
    global videosCollection
    try:
        if videosCollection is None: # Database not connected
            create_connection() # Connect the database
        
        if len(videos) == 0:
            print("WARNING: The video list is empty. Skipping Insertion")
            return

        videosCollection.insert_many(create_posts(videos))
        print("SUCCESS: Inserting Videos into database successful.")
    except Exception as e:
        print("ERROR Inserting videos: {0}".format(str(e)))
        raise e

def delete_all_videos():

    """
    Delete all the videos from the database
    :return: None
    """
    global videosCollection
    try:
        if videosCollection is None: # Database not connected
            create_connection() # Connect the database
        
        videosCollection.delete_many({})
        print("SUCCESS: All videos deleted from database.")
    except Exception as e:
        print("ERROR Deleting videos: {0}".format(str(e)))
        raise e


def adapt_data(data):
    metadata = {
        "nexPageToken": data["nextPageToken"]
    }
    videos = []
    for item in data["items"]:
        video = Video(
            item["id"]["videoId"],
            item["snippet"]["title"],
            item["snippet"]["description"],
            item["snippet"]["publishedAt"],
            item["snippet"]["thumbnails"]["high"]["url"]
        )
        videos.append(video)
    return metadata, videos


def sync_db_with_yt(url, query, api_key, published_after, max_results):
    """
    Synchronises the db with the latest videos fetched from the Youtube API
    :return: None
    """

    try:
        # Fetching the latest videos
        request_url = url.format(
            api_key=api_key,
            query=query,
            published_after=published_after,
            max_results=max_results
        )
        print(request_url)
        response = requests.request("GET", request_url)
        content = (response.content).decode("UTF-8")
        # print(content[:500])
        
        # For testing puposes only
        # with open(os.path.join(sys.path[0], "app/sample_data.json"), "r") as json_file:
        print("TYPE {}".format(type(content)))
        data = json.loads(content)
        metadata, videos = adapt_data(data)

        delete_all_videos()
        insert_videos(videos)

        # Parsing the videos and extracting the necessary data

        # Putting the parsed data into db
    except Exception as e:
        print("ERROR: Synchronising Failed -> {}".format(str(e)))
        raise e


def get_videos_from_db(page_number, max_results):
    """
    GET videos from the database
    :return: videos, response message, total pages, page number
    """
    global videosCollection
    try:
        if videosCollection is None: # Database not connected
            create_connection() # Connect the database
        
        videos = list(videosCollection.find().sort("publishedAt", -1))
        total_pages = Math.ceil(len(videos) / max_results)

        response_msg = "success"
        if page_number < 1 or page_number > total_pages:
            response_msg = "failed: Invalid pageNumber provided. Returning the first page."
            page_number = 1
        start = max_results * (page_number-1)
        videos = videos[start : start + max_results]
        print("SUCCESS: Getting Videos from database successful.")
        return videos, response_msg, total_pages, page_number
    
    except Exception as e:
        response_msg = "failed: Getting videos from DB: {0}".format(str(e))
        return [], response_msg, 0, 1


def search_videos_from_db(query, page_number, max_results):
    """
    Search videos from the database
    :return: videos, response message, total pages, page number
    """
    global videosCollection
    try:
        if videosCollection is None: # Database not connected
            create_connection() # Connect the database
        
        print(f"Searching for '{query}'")
        videosCollection.drop_indexes()
        videosCollection.create_index([('title', TEXT), ('description', TEXT)], name="desc_index")
        videos = list(videosCollection.find({"$text": {"$search": query}}).sort('publishedAt', -1))
        total_pages = Math.ceil(len(videos) / max_results)

        response_msg = "success"
        if page_number < 1 or page_number > total_pages:
            response_msg = "failed: Invalid pageNumber provided. Returning the first page."
            page_number = 1
        start = max_results * (page_number-1)
        videos = videos[start : start + max_results]
        print("SUCCESS: Getting Videos from database successful.")
        return videos, response_msg, total_pages, page_number
    
    except Exception as e:
        response_msg = "failed: Getting videos from DB: {0}".format(str(e))
        print(e)
        return [], response_msg, 0, 1


if __name__ == '__main__':
    pass