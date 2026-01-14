import json
import os
import config

from gmail_service import get_gmail_service
from sheets_service import get_sheets_service, append_rows
from email_parser import extract_email_data


def load_state():
    if not os.path.exists(config.STATE_FILE):
        return 0
    with open(config.STATE_FILE, "r") as f:
        return json.load(f).get("last_ts", 0)


def save_state(ts):
    with open(config.STATE_FILE, "w") as f:
        json.dump({"last_ts": ts}, f)


def main():
    last_ts = load_state()

    gmail = get_gmail_service(config.SCOPES)
    sheets = get_sheets_service(config.SCOPES)

    if last_ts == 0:
        query = "is:unread in:inbox"
    else:
        query = f"is:unread in:inbox after:{last_ts // 1000}"

    results = gmail.users().messages().list(
        userId="me",
        q=query
    ).execute()

    messages = results.get("messages", [])
    rows = []
    max_ts = last_ts

    for msg in messages:
        data = gmail.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        parsed = extract_email_data(data)

        rows.append([
            parsed["from"],
            parsed["subject"],
            parsed["date"],
            parsed["content"]
        ])

        max_ts = max(max_ts, parsed["timestamp"])

        gmail.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

    if rows:
        append_rows(
            sheets,
            config.SPREADSHEET_ID,
            config.SHEET_NAME,
            rows
        )
        save_state(max_ts)


if __name__ == "__main__":
    main()
