import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def get_gmail_service(scopes):
    creds = None

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    creds_path = os.path.join(base_dir, "credentials", "credentials.json")
    token_path = os.path.join(base_dir, "token.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)

        print("\n Opening browser for Gmail OAuth login...\n")
        creds = flow.run_local_server(
            port=0,
            open_browser=True
        )

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)
