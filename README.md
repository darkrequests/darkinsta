# For any questions 
whatsapp me {0791258754}

# Instagram Scraper Tool

The Instagram Scraper Tool is a command-line application that allows users to scrape public data from Instagram profiles. Users can log in using their session ID and retrieve information such as profile details, followers, and following lists for a target username.

## Features

- **Login with Session ID**: Authenticate securely using your Instagram session ID.
- **Profile Information Extraction**: Retrieve details like email and phone number (if available).
- **Followers and Following List**: Fetch up to 100 followers and following for demonstration purposes (adjustable).
- **Interactive Menu**: Choose specific actions, such as extracting profile information, followers, following, or both.

## Prerequisites

### 1. Python

Ensure you have Python 3.8 or higher installed. You can download Python from [python.org](https://www.python.org/).

### 2. Required Libraries

Install the required Python libraries using pip:

```bash
pip install requests instagram-scraper
```

### 3. Session ID

You need your Instagram session ID to authenticate. This can be retrieved from your browser's developer tools:
- Log in to Instagram via your browser.
- Open developer tools (usually `F12` or `Ctrl+Shift+I`).
- Navigate to the "Application" tab and find the `sessionid` cookie under "Storage > Cookies".

## Installation

Clone this repository or download the script:
https://github.com/darkrequests/darkinsta/
```bash
git clone https://github.com/darkrequests/darkinsta.git
cd darkinsta
```

## Usage

Run the script from the command line:

```bash
python insta.py
```

### Steps:

1. Enter your Instagram session ID when prompted.
2. Enter the target username whose data you want to scrape.
3. Choose an option from the menu:
   - **1**: Extract profile information.
   - **2**: Extract followers and following lists.
   - **3**: Extract both profile information and followers/following.
4. View the results in the terminal.

## Configuration

### Adjusting the Number of Followers/Following

The script limits the number of followers and following fetched to 100 by default for demonstration. To change this:

- Open the script file.
- Locate the `extract_followers_and_following` function.
- Modify the second parameter of `scraper.get_followers()` and `scraper.get_following()` (e.g., `10000` for maximum results).

## Example Output

### Profile Information:

```
--- Profile Information ---
Username: target_username
Phone Number: Not Available
Email: example@domain.com
```

### Followers:

```
Followers: 3 found
- follower1
- follower2
- follower3
```

### Following:

```
Following: 2 found
- following1
- following2
```



This tool is for educational and personal use only. Use it responsibly and ensure you comply with all applicable laws and platform terms.

