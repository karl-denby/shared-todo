from pymongo import MongoClient
from multiprocessing import Queue, Process
import ssl, os
import datetime

cluster = ''  # Connection String
output = Queue()  # Message Queue for threads to load

def create_note(connection = 'mongodb://localhost:27017', post = {}):
    
    # Create connection
    client = MongoClient(connection)    
    db = client['shared']
    col = db['todo']
    
    # Insert data
    return col.insert_one(post).inserted_id

#
# Goal: cli to add todo items to a mongodb collection hosted on Atlas
# Current: just performs a threaded drop/insert of 1000 records
#
if __name__ == "__main__":
    
    # check we have a connection string
    if cluster == '':
        print("No connection string defined in 'cluster' variable.  ABORTING.")
        exit()
    
    note = {
        "title": "Example Note",
        "text": "This is some sample text to represent the body of a document",
        "tags": ["important", "work"],
        "attributes" : [
            { "color": "red" },
            { "pinned": True }
        ],
        "created": datetime.datetime.utcnow(), 
        "expires": datetime.datetime.utcnow()
    }

    print("Creating Note")
    create_note(cluster, note)
    print("Done")
