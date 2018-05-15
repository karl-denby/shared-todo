import os
from dotenv import load_dotenv

from pymongo import MongoClient
from multiprocessing import Queue, Process
import ssl, os
import datetime
import argparse

load_dotenv()

'''
    Functions
'''
def create_note(connection = os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://localhost:27017'), post = {}):
    
    # Create connection
    client = MongoClient(connection)
    db = client['shared']
    col = db['todo']
    
    # Insert data
    return col.insert_one({}).inserted_id

'''
    Constants
'''
NOTE = {
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


'''
    Goal: cli to add todo items to a mongodb collection hosted on Atlas
    Current: just performs a threaded drop/insert of 1000 records
'''

output = Queue()  # Message Queue for threads to load

if __name__ == "__main__":    

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=['create', 'list', 'modify', 'delete'],
        help="Action: default is create if no action is specified"
    )
    
    args = parser.parse_args()
    
    if args.action  == None:
        action = 'create'
    else:
        action = args.action

    if action == 'create':
        print('create a note')
        create_note(NOTE)
    elif action == 'list':
        print('list of notes')
    elif action == 'modify':
        print('change a note')
    elif action == 'delete':
        print('delete a note')
    