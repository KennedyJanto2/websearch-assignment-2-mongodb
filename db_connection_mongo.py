#-------------------------------------------------------------------------
# AUTHOR: kennedy janto
# FILENAME: db_connection_mongo.py
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #2
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
from pymongo import MongoClient

def connectDataBase():

    # Create a database connection object using pymongo
    client = MongoClient('localhost', 27017)
    db = client.corpus
    col = db.documents
    return db, col

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    term_count = {}
    words = docText.split()
    for word in words:
        word = word.lower()
        if word not in term_count:
            term_count[word] = 1
        else:
            term_count[word] += 1

    # create a list of dictionaries to include term objects.
    term_objects = [{"term": k, "count": v} for k, v in term_count.items()]

    #Producing a final document as a dictionary including all the required document fields
    doc = {
        "_id": docId,
        "text": docText,
        "title": docTitle,
        "date": docDate,
        "category": docCat,
        "terms": term_objects
    }

    # Insert the document
    col.insert_one(doc)

def deleteDocument(col, docId):

    # Delete the document from the database
    col.delete_one({"_id": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    deleteDocument(col, docId)

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    inverted_index = {}
    cursor = col.find({})

    for document in cursor:
        for term_obj in document["terms"]:
            term = term_obj["term"]
            count = term_obj["count"]
            title = document["title"]
            
            if term not in inverted_index:
                inverted_index[term] = {}
            
            inverted_index[term][title] = count

    # Formatting the output as per the given example
    output_index = {}
    for term, titles in inverted_index.items():
        output_str = ",".join([f"{title}:{count}" for title, count in titles.items()])
        output_index[term] = output_str

    return output_index