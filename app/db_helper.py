# import pymongo
from pymongo import MongoClient

videosCollection = None

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


def insert_video():
    global videosCollection
    # create_connection()
    video = {
        "_id": 3,
        "title" : "Sample Title", 
        "description": "Sample Description",
        "publishedAt" : "2021-05-21 19:45:22",
        "thumbnailUrl" : "https://blah.com"
    }

    print("videosCollection is: {0}".format(videosCollection))
    try:
        videosCollection.insert_one(video)
    except Exception as e:
        print("ERROR inserting video: {0}".format(str(e)))

if __name__ == '__main__':
    # videosCollection = create_connection()
    create_connection()
    insert_video()