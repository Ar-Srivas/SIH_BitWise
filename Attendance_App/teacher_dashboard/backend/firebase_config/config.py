import firebase_admin
from firebase_admin import credentials, firestore

import os

path = os.path.join(os.path.dirname(__file__), "..", "credentials.json")
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)

db = firestore.client()
# print(db)