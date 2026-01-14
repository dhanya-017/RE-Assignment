import base64
from email.utils import parsedate_to_datetime

MAX_CELL_LENGTH = 45000  # Safe limit below Google Sheets max (50k)


def extract_email_data(message):
    headers = message["payload"]["headers"]
    payload = message["payload"]

    def get_header(name):
        for h in headers:
            if h["name"] == name:
                return h["value"]
        return ""

    body = ""
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and "data" in part["body"]:
                body = base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8", errors="ignore")
                break
    else:
        if "data" in payload["body"]:
            body = base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode("utf-8", errors="ignore")

    content = body.strip()

    #Truncate content to avoid Google Sheets 50k char limit
    if len(content) > MAX_CELL_LENGTH:
        content = content[:MAX_CELL_LENGTH] + "\n\n[Content truncated]"

    return {
        "from": get_header("From"),
        "subject": get_header("Subject"),
        "date": get_header("Date"),
        "timestamp": int(message["internalDate"]),
        "content": content
    }
