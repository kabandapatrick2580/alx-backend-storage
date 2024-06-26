#!/usr/bin/env python3
"""
Script to provide stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def print_logs_stats(collection):
    """
    Print stats about Nginx logs stored in MongoDB.

    :param collection: pymongo collection object
    """
    # Total number of logs
    total_logs = collection.count_documents({})
    print("{} logs".format(total_logs))
    print("Methods:")

    # Methods stats
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print("    method {}: {}".format(method, count))

    # Status check stats
    status_check_count = collection.count_documents(
            {"method": "GET", "path": "/status"})
    print("{} status check".format(status_check_count))

    # Top 10 IPs
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    for ip_doc in collection.aggregate(pipeline):
        print(f"    {ip_doc['_id']}: {ip_doc['count']}")


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Print logs stats
    print_logs_stats(collection)
