import os
import json
from dotenv import load_dotenv

load_dotenv()

creds = {
    "type": "service_account",
    "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", "asi-resh"),
    "private_key_id": "manual-key",
    "private_key": os.environ.get("GOOGLE_CLOUD_PRIVATE_KEY", "").replace("\\n", "\n"),
    "client_email": os.environ.get("GOOGLE_CLOUD_CLIENT_EMAIL", ""),
    "client_id": "",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.environ.get('GOOGLE_CLOUD_CLIENT_EMAIL', '').replace('@', '%40')}"
}

with open("c:/Universal_Lab_AP_Phillips/scratch/credentials.json", "w") as f:
    json.dump(creds, f, indent=2)

print("Generated credentials.json")
