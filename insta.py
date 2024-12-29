import os
import logging
import requests
from instagram_scraper import InstagramScraper

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def login_to_instagram(session_id):
    """
    Logs into Instagram using the provided session ID.
    Args:
        session_id (str): The session ID for Instagram authentication.
    Returns:
        bool: True if login is successful, False otherwise.
    """
    url = "https://www.instagram.com/accounts/login/ajax/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/80.0.3987.132 Safari/537.36"
        ),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "Cookie": f"sessionid={session_id}",
    }

    try:
        logging.info("Attempting to log in to Instagram...")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logging.info("Login successful!")
            return True
        else:
            logging.error("Login failed. Please check your session ID.")
            return False
    except requests.RequestException as e:
        logging.error("An error occurred during login: %s", e)
        return False


def extract_profile_info(username, scraper):
    """
    Extracts profile information such as phone number and email.
    Args:
        username (str): Instagram username.
        scraper (InstagramScraper): Authenticated Instagram scraper instance.
    """
    try:
        logging.info("Fetching profile information for '%s'...", username)
        profile = scraper.get_account(username)
        phone_number = profile.get("phone_number", "Not Available")
        email = profile.get("email", "Not Available")

        logging.info("\n--- Profile Information ---")
        logging.info("Username: %s", username)
        logging.info("Phone Number: %s", phone_number)
        logging.info("Email: %s", email)
    except Exception as e:
        logging.error("Failed to extract profile info: %s", e)


def extract_followers_and_following(username, scraper):
    """
    Extracts followers and following list for a given username.
    Args:
        username (str): Instagram username.
        scraper (InstagramScraper): Authenticated Instagram scraper instance.
    """
    try:
        logging.info("Fetching followers for '%s'...", username)
        followers = scraper.get_followers(username, 100, delayed=True)  # Fetch up to 100 followers
        logging.info("Followers: %d found", len(followers))
        for follower in followers:
            logging.info(f"- %s", follower)

        logging.info("Fetching following for '%s'...", username)
        following = scraper.get_following(username, 100, delayed=True)  # Fetch up to 100 following
        logging.info("Following: %d found", len(following))
        for following_user in following:
            logging.info(f"- %s", following_user)
    except Exception as e:
        logging.error("Failed to extract followers/following: %s", e)


def get_session_id():
    """
    Prompts the user for a session ID securely.
    Returns:
        str: The entered session ID.
    """
    session_id = input("Enter your Instagram session ID (hidden input): ").strip()
    if not session_id:
        raise ValueError("Session ID cannot be empty.")
    return session_id


def get_target_username():
    """
    Prompts the user for the target username to scrape.
    Returns:
        str: The entered target username.
    """
    username = input("Enter the target Instagram username to scrape: ").strip()
    if not username:
        raise ValueError("Target username cannot be empty.")
    return username


def display_menu():
    """
    Displays options to the user and prompts for a choice.
    Returns:
        int: The chosen menu option.
    """
    print("\nOptions:")
    print("1. Extract profile information")
    print("2. Extract followers and following")
    print("3. Extract both")
    choice = input("Enter your choice (1/2/3): ").strip()
    if choice not in {"1", "2", "3"}:
        raise ValueError("Invalid choice. Please enter 1, 2, or 3.")
    return int(choice)


def main():
    """
    Main function to handle Instagram scraping.
    """
    print("Welcome to the Instagram Scraper Tool!")
    try:
        # Get session ID and target username
        session_id = get_session_id()
        target_username = get_target_username()

        # Attempt login
        if login_to_instagram(session_id):
            scraper = InstagramScraper(target_username)
            scraper.authenticate_with_login()
            print("\nLogged in successfully. Proceeding to scrape data...")

            # Display menu and handle user's choice
            choice = display_menu()
            if choice == 1:
                extract_profile_info(target_username, scraper)
            elif choice == 2:
                extract_followers_and_following(target_username, scraper)
            elif choice == 3:
                extract_profile_info(target_username, scraper)
                extract_followers_and_following(target_username, scraper)

            print("\nScraping complete. Thank you for using the tool!")
        else:
            print("Login failed. Please check your session ID and try again.")
    except Exception as e:
        logging.error("An error occurred: %s", e)
        print("An error occurred. Please check the logs for details.")


if __name__ == "__main__":
    main()
