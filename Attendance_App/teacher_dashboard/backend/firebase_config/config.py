import firebase_admin
from firebase_admin import credentials, firestore
import os
import base64
import json

cred_base64 = os.environ.get("FIREBASE_CREDENTIALS")
if cred_base64:
    cred_json = base64.b64decode(cred_base64).decode("utf-8")
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
else:
    print("WARNING: FIREBASE_CREDENTIALS_BASE64 not found. Falling back to local key file.")
    path = os.path.join(os.path.dirname(__file__), "..", "credentials.json")
    cred = credentials.Certificate(path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
# print(db)