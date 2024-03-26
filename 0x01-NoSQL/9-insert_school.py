#!/usr/bin/env python3
"""9-insert_school.py module. """
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into the specified MongoDB
    collection using keyword arguments.

    Parameters:
    - mongo_collection: pymongo.collection.Collection
        The pymongo collection object representing the
        collection where the new document will be inserted.
    - **kwargs: dict
        Keyword arguments representing the fields and
        values of the new document.

    Returns:
    - ObjectId
        The ObjectId (_id) of the inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
