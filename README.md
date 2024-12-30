# Instagram osintTool
# Contact me
 Whatsapp{0791258754}
## Overview
The **Instagram osint Tool** is a Python script that allows users to extract public and private information from Instagram profiles using a session ID for authentication. It supports fetching:

- Profile details (e.g., email and phone number, if available)
- Follower and following counts

## Features
- **Session Authentication**: Logs into Instagram using a session ID.
- **Profile Data Extraction**: Retrieves basic profile information, such as phone number and email (if accessible).
- **Followers and Following Count**: Fetches the count of followers and accounts followed by the user.
- **Menu-Driven Interface**: Allows users to choose the type of data they wish to scrape.

## Requirements
- Python 3.7 or later
- Internet connection
- Valid Instagram session ID

## Installation
1. Clone the repository or download the script:
   ```bash
   git clone https://github.com/darkrequests/darkinsta.git
   cd darkinsta
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script using the following format:
```bash
python3 insta.py <session_id> <csrf_token> <username>
```

### Example
```bash
python3 insta.py YOUR_SESSION_ID CSRF_TOKEN target_username
```

### Input Options
After running the script, you'll be prompted to select an option from the menu:
: Extract profile information

## Notes
- **Session ID**: Obtain your Instagram session ID by inspecting your browser's cookies for Instagram after logging in.
- **CSRF Token**: Automatically handled by the script.
- This script adheres to Instagram's API limitations. Ensure you use it responsibly and within legal boundaries.

## Disclaimer
This tool is intended for educational purposes only. Unauthorized scraping of data may violate Instagram's terms of service or applicable laws. Use responsibly and at your own risk.

(https://files.fm/u/ycwwwzqkym)


