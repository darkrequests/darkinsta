import logging
import requests
import sys
import json

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def initialize_session(session_id, csrf_token):
    """Initializes a session object with session ID and CSRF token."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Instagram 133.0.0.34.124 Android (28/9; 320dpi; 720x1280; Xiaomi; Redmi 5; rosy; qcom; en_US)",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.instagram.com",
        "Connection": "keep-alive",
        "Referer": "https://www.instagram.com/",
        "TE": "trailers",
    })
    session.cookies.update({
        "csrftoken": csrf_token,
        "sessionid": session_id,
        "ig_nrcb": "1",
    })
    return session

def validate_session(session):
    """Load Instagram website to validate session."""
    url = "https://www.instagram.com/"
    try:
        logging.info("Loading Instagram website to validate session...")
        response = session.get(url)
        if response.status_code == 200:
            logging.info("Instagram website loaded successfully.")
            return True
        else:
            logging.error("Failed to load Instagram website. Status code: %d", response.status_code)
            return False
    except requests.RequestException as e:
        logging.error("An error occurred while loading Instagram website: %s", e)
        return False

def extract_profile_info(session, username):
    """
    Extracts profile information using the user's profile page.
    Args:
        session (requests.Session): Authenticated session for Instagram.
        username (str): Instagram username.
    """
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

    try:
        logging.info("Fetching profile information for '%s'...", username)
        response = session.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                user = data.get("data", {}).get("user", {})
                phone_number = user.get("business_contact_phone", "Not Available")
                email = user.get("public_email", "Not Available")
                followers = user.get("edge_followed_by", {}).get("count", "Not Available")
                following = user.get("edge_follow", {}).get("count", "Not Available")

                logging.info("\n--- Profile Information ---")
                logging.info("Username: %s", username)
                logging.info("Phone Number: %s", phone_number)
                logging.info("Email: %s", email)
                logging.info("Followers: %s", followers)
                logging.info("Following: %s", following)
            except json.JSONDecodeError:
                logging.error("Failed to decode JSON response.")
        else:
            logging.error("Failed to fetch profile info. Status code: %d", response.status_code)
            logging.error("Response content: %s", response.content)
    except requests.RequestException as e:
        logging.error("An error occurred while fetching profile info: %s", e)

def main():
    """Main function to handle Instagram scraping."""
    setup_logging()

    if len(sys.argv) < 4:
        print("Usage: python insta.py <session_id> <csrf_token> <username>")
        sys.exit(1)

    session_id = sys.argv[1]
    csrf_token = sys.argv[2]
    username = sys.argv[3]

    try:
        session = initialize_session(session_id, csrf_token)
        if validate_session(session):
            logging.info("Session validated. Proceeding to fetch data...")
            extract_profile_info(session, username)
        else:
            logging.error("Failed to validate session. Please check credentials.")
    except Exception as e:
        logging.error("An error occurred: %s", e)

if __name__ == "__main__":
    main()
