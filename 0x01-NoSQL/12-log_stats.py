#!/usr/bin/env python3
"""Script to provide statistics about Nginx logs stored in MongoDB."""

from pymongo import MongoClient


def log_stats():
    """Print statistics about Nginx logs stored in MongoDB."""
    # Connect to the MongoDB instance
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Access the logs database and the nginx collection
    db = client.logs
    collection = db.nginx

    # Count the number of documents in the collection
    total_logs = collection.count_documents({})

    # Count the number of documents with each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents(
        {"method": method}) for method in methods}

    # Count the number of documents with method=GET and path=/status
    status_check = collection.count_documents(
        {"method": "GET", "path": "/status"})

    # Print the statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check} status check")
