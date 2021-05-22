# import pymongo
from pymongo import MongoClient
from app.models.video import Video

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
                "published_at": video.published_at,
                "thumbnail_url": video.thumbnail_url
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


def sync_db_with_yt(url, query, api_key, published_after, max_results):
    """
    Synchronises the db with the latest videos fetched from the Youtube API
    :return: None
    """
    # Fetching the latest videos
    request_url = url.format(
        api_key=api_key,
        query=query,
        published_after=published_after,
        max_results=max_results
    )
    print(request_url)

    # Parsing the videos and extracting the necessary data

    # Putting the parsed data into db


if __name__ == '__main__':
    pass