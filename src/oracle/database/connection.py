import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


if os.getenv("ENVIRONMENT", "dev") == "dev":
    credential_path = "firebase_credentials_dev.json"
else:
    credential_path = "firebase_credentials_prod.json"

cred = credentials.Certificate(credential_path)
firebase_admin.initialize_app(cred)


def get_db_client():
    return firestore.client()
