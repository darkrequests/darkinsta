import os
import logging
import requests
import sys
from getpass import getpass

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def initialize_session(session_id):
    """Initializes a session object with session ID and CSRF token."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/80.0.3987.132 Safari/537.36"
        ),
    })
    session.cookies.set("sessionid", session_id)

    # Fetch CSRF token
    try:
        logging.info("Fetching CSRF token...")
        response = session.get("https://www.instagram.com")
        csrf_token = response.cookies.get("csrftoken")
        if csrf_token:
            session.headers.update({"X-CSRFToken": csrf_token})
            logging.info("CSRF token retrieved successfully.")
        else:
            logging.error("Failed to retrieve CSRF token.")
    except requests.RequestException as e:
        logging.error("An error occurred while initializing session: %s", e)
        raise

    return session

def login_to_instagram(session):
    """Validates Instagram session by checking login status."""
    url = "https://www.instagram.com/accounts/login/ajax/"
    try:
        logging.info("Validating Instagram session...")
        response = session.get(url)
        if response.status_code == 200:
            logging.info("Session is valid.")
            return True
        else:
            logging.error("Invalid session. Please check your session ID.")
            return False
    except requests.RequestException as e:
        logging.error("An error occurred during login validation: %s", e)
        return False

def extract_profile_info(session, username):
    """Extracts Instagram profile information for a given username."""
    url = f"https://www.instagram.com/{username}/?__a=1"
    try:
        logging.info("Fetching profile information for '%s'...", username)
        response = session.get(url)
        if response.status_code == 200:
            data = response.json()
            user = data.get("graphql", {}).get("user", {})
            phone_number = user.get("phone_number", "Not Available")
            email = user.get("email", "Not Available")

            logging.info("\n--- Profile Information ---")
            logging.info("Username: %s", username)
            logging.info("Phone Number: %s", phone_number)
            logging.info("Email: %s", email)
        else:
            logging.error("Failed to fetch profile info. Status code: %d", response.status_code)
    except requests.RequestException as e:
        logging.error("An error occurred while fetching profile info: %s", e)

def extract_followers_and_following(session, username):
    """Extracts followers and following counts for a given username."""
    url = f"https://www.instagram.com/{username}/"
    try:
        logging.info("Fetching followers and following for '%s'...", username)
        response = session.get(url)
        if response.status_code == 200:
            data = response.text
            followers_start = data.find('"edge_followed_by":{"count":') + len('"edge_followed_by":{"count":')
            followers_end = data.find('}', followers_start)
            followers_count = data[followers_start:followers_end]

            following_start = data.find('"edge_follow":{"count":') + len('"edge_follow":{"count":')
            following_end = data.find('}', following_start)
            following_count = data[following_start:following_end]

            logging.info("Followers: %s", followers_count)
            logging.info("Following: %s", following_count)
        else:
            logging.error("Failed to fetch followers and following. Status code: %d", response.status_code)
    except requests.RequestException as e:
        logging.error("An error occurred while fetching followers and following: %s", e)

def display_menu():
    """Displays options to the user and prompts for a choice."""
    print("\nOptions:")
    print("1. Extract profile information")
    print("2. Extract followers and following")
    print("3. Extract both")
    choice = input("Enter your choice (1/2/3): ").strip()
    if choice not in {"1", "2", "3"}:
        raise ValueError("Invalid choice. Please enter 1, 2, or 3.")
    return int(choice)

def main():
    """Main function to handle Instagram scraping."""
    setup_logging()

    if len(sys.argv) < 3:
        print("Usage: python insta.py <session_id> <username>")
        sys.exit(1)

    session_id = sys.argv[1]
    target_username = sys.argv[2]

    try:
        # Initialize session and validate login
        session = initialize_session(session_id)
        if login_to_instagram(session):
            print("\nLogged in successfully. Proceeding to scrape data...")

            # Display menu and handle user's choice
            choice = display_menu()
            if choice == 1:
                extract_profile_info(session, target_username)
            elif choice == 2:
                extract_followers_and_following(session, target_username)
            elif choice == 3:
                extract_profile_info(session, target_username)
                extract_followers_and_following(session, target_username)

            print("\nScraping complete. Thank you for using the tool!")
        else:
            print("Login failed. Please check your session ID and try again.")
    except Exception as e:
        logging.error("An error occurred: %s", e)
        print("An error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()
