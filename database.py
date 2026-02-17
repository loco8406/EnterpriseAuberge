import requests
import os

class Database:
    def __init__(self):
        self.firebase_url = os.environ.get("FIREBASE_DB")
    
    def clear(self):
        """Clear all guardrails from Firebase"""
        if self.firebase_url:
            requests.delete(f"{self.firebase_url}/guardrails.json")

db = Database()