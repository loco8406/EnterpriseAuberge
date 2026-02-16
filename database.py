import requests
import os

class Database:
    def __init__(self):
        self.firebase_url = os.environ.get(
            "FIREBASE_DB",
            "https://ecm3408-ca-ff1bd-default-rtdb.europe-west1.firebasedatabase.app"
        )
    
    def clear(self):
        """Clear all guardrails from Firebase"""
        if self.firebase_url:
            requests.delete(f"{self.firebase_url}/guardrails.json")

db = Database()