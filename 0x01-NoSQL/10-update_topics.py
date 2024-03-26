#!/usr/bin/env python3
"""10-update_topics.py module. """
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Update all topics of a school document based on the school name.

    Parameters:
    - mongo_collection: pymongo.collection.Collection
        The pymongo collection object representing the
        collection containing the school documents.
    - name: str
        The name of the school to update.
    - topics: list of str
        The list of topics approached in the school.

    Returns:
    - int
        The number of documents updated.
    """
    # Ensure topics is a list
    if not isinstance(topics, list):
        raise TypeError("Topics must be a list of strings.")

    # Update documents with the specified school name
    result = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )

    return result.modified_count
