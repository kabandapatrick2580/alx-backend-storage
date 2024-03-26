#!/usr/bin/env python3
""" 8-all module. """

import pymongo


def list_all(mongo_collection):
    """
    List all documents in the specified MongoDB collection.

    Parameters:
    - mongo_collection: pymongo.collection.Collection
        The pymongo collection object representing the collection
        from which documents will be retrieved.

    Returns:
    - list of dict
        A list containing all documents in the collection.
        Each document is represented as a dictionary.
        If the collection is empty or mongo_collection is None,
        an empty list is returned.
    """
    if mongo_collection is None:
        return []
    return list(mongo_collection.find())
