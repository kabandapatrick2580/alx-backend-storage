#!/usr/bin/env python3
"""11-schools_by_topic.py module."""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Retrieve a list of schools that have a specific topic.

    Parameters:
    - mongo_collection: pymongo.collection.Collection
        The pymongo collection object representing the collection of schools.
    - topic: str
        The topic to search for.

    Returns:
    - list of dict
        A list of schools that have the specified topic.
    """
    # Query the collection to find schools with the specified topic
    schools = mongo_collection.find({"topics": topic})

    # Convert the cursor to a list of dictionaries
    return list(schools)
