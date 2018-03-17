from pymongo import MongoClient
from multiprocessing import Queue, Process
import ssl
import time
import os

cluster = ''  # Connection String
output = Queue()  # Message Queue for threads to load


def insert_process(connection = 'mongodb+srv://localhost:27017', thread = 0, start = 0, end = 100, mqueue=output):
    
    # Create connection for this thread
    client = MongoClient(connection)    
    db = client['shared-todo']
    col = db['shared-todo']

    # drop any existing data
    col.drop()
    
    # Insert some data
    document_id = start
    while(document_id < end):
        post = {"_id": document_id}
        col.insert_one(post).inserted_id
        document_id = document_id + 1
    
    # Store results of execution
    mqueue.put("T" + str(thread) + ": inserted from " + str(start) + " to " + str(document_id))

#
# Goal: cli to add todo items to a mongodb collection hosted on Atlas
# Current: just performs a threaded drop/insert of 1000 records
#
if __name__ == "__main__":
    # check we have a connection string
    if cluster == '':
        print("No connection string defined in 'cluster' variable.  ABORTING.")
        exit()

    process1 = Process(target=insert_process, args=(cluster, 1, 1, 250, output))
    process2 = Process(target=insert_process, args=(cluster, 2, 250, 500, output))
    process3 = Process(target=insert_process, args=(cluster, 3, 500, 750, output))
    process4 = Process(target=insert_process, args=(cluster, 4, 750, 1000, output))

    # Start all threads and wait for them to finish
    processes = [process1, process2, process3, process4]

    for p in processes: 
        p.start()
        print("Insert process running: " + str(p.pid))

    for p in processes:
        p.join()

    # Summarize work that has been done
    for p in processes:
        results = output.get()
        print(results)