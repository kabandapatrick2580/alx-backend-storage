#!/usr/bin/env python3
"""
A Python function that returns all students sorted by average score.
"""


def top_students(mongo_collection):
    """
    Return all students sorted by average score.

    Parameters:
    - mongo_collection: pymongo.collection.Collection
        The pymongo collection object representing the collection of students.

    Returns:
    - list of dict
        A list containing all students with their average scores,
        sorted in descending order by average score.
    """
    pipeline = [
        {
            "$addFields": {
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]

    return list(mongo_collection.aggregate(pipeline))
