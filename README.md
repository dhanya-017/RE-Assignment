Gmail to Google Sheets Automation (Python)

Author: Dhanya Dwivedi
Language: Python 3
APIs Used: Gmail API, Google Sheets API
Authentication: OAuth 2.0 (Installed Application Flow)

📖 Project Overview

This project implements a Python automation system that reads real incoming unread emails from a Gmail inbox using the Gmail API and logs them into a Google Sheet using the Google Sheets API.

Each qualifying email is appended as a new row in a Google Sheet with the following fields:

Column	Description
From	Sender email address
Subject	Email subject
Date	Date & time received
Content	Plain-text email body

The system ensures:

Secure authentication via OAuth 2.0

No duplicate processing

Persistent state across executions

🏗 High-Level Architecture Diagram
+----------------+
|   Gmail Inbox  |
+--------+-------+
         |
         | Gmail API (OAuth 2.0)
         v
+------------------------+
| Python Automation App  |
|                        |
| - Fetch unread emails  |
| - Parse content        |
| - Track last state     |
+------------+-----------+
             |
             | Google Sheets API
             v
+------------------------+
| Google Sheet           |
| (Append rows only)     |
+------------------------+

⚙️ Step-by-Step Setup Instructions
1. Clone Repository
git clone <your-repository-link>
cd gmail-to-sheets

2. Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Google Cloud Configuration

Create a project in Google Cloud Console

Enable:

Gmail API

Google Sheets API

Configure OAuth Consent Screen (External)

Create OAuth Client ID → Desktop Application

Download credentials.json

📂 Place the file here:

credentials/credentials.json


🚫 Do NOT commit this file

5. Configure Google Sheet

Create a Google Sheet and copy only the spreadsheet ID.

Update config.py:

SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"
SHEET_NAME = "Sheet1"

6. Run the Script
python src/main.py


First run triggers OAuth consent

Subsequent runs reuse saved token

🔐 OAuth Flow Explanation

Uses OAuth 2.0 Installed App Flow

User explicitly grants permission via browser

Tokens are stored locally in token.json

Tokens are reused on future runs

Why OAuth instead of Service Account?

Gmail API requires user-level consent

Service accounts cannot access personal inboxes

🔁 Duplicate Prevention Logic

Duplicates are prevented using two mechanisms:

Unread-only email filtering

is:unread


State persistence

Timestamp of last processed email is stored

Only emails received after this timestamp are processed

This guarantees idempotent execution.

💾 State Persistence Method

State is stored in a local file:

state.json


Example:

{
  "last_ts": 1705234567890
}


Why this approach?

Lightweight and fast

No database required

Human-readable

Reliable across script executions

🧩 Challenges Faced & Solutions
1. OAuth flow blocking execution

Solution: Explicit browser-based OAuth handling with token reuse.

2. Gmail query returning no emails

Solution: Handled first-run logic separately and adjusted Gmail search filters.

3. Google Sheets cell size limit (50,000 chars)

Solution: Implemented safe truncation of email content before insertion.

⚠️ Limitations

Long email bodies are truncated

Attachments are not processed

HTML formatting is not preserved

Extremely large inbox pagination is not handled

## 🎥 Demo Video

A 2–3 minute screen recording demonstrating:
- Project flow
- Gmail to Google Sheets data movement
- Duplicate prevention logic
- Script behavior on repeated execution

📹 Video Link: https://drive.google.com/file/d/1XVmPwzkuEN_4LvmUorHHcAAGNwUxyzcI/view?usp=sharing , https://drive.google.com/file/d/1lBiTEOQJUCQEzNd7lAWr8ekxLg2QCy80/view?usp=sharing