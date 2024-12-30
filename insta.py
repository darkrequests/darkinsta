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
                
                profile_info = {
                    "Username": username,
                    "Profile ID": user.get("id"),
                    "Profile Picture URL": user.get("profile_pic_url_hd"),
                    "Bio": user.get("biography"),
                    "Full Name": user.get("full_name"),
                    "Website": user.get("external_url"),
                    "Private Account": user.get("is_private"),
                    "Verified Account": user.get("is_verified"),
                    "Business Account": user.get("is_business_account"),
                    "Gender": user.get("gender"),
                    "Category": user.get("category_name"),
                    "Joined Date": user.get("joined_date"),
                    "Highlights Count": user.get("highlight_reel_count"),
                    "Story Views Count": user.get("story_views_count"),
                    "IGTV Videos Count": user.get("total_igtv_videos"),
                    "Tagged Posts Count": user.get("tagged_posts_count"),
                    "Activity Status": user.get("activity_status"),
                    "Phone Number": user.get("business_contact_phone"),
                    "Email": user.get("public_email"),
                    "Followers Count": user.get("edge_followed_by", {}).get("count"),
                    "Following Count": user.get("edge_follow", {}).get("count"),
                    "Media Count": user.get("edge_owner_to_timeline_media", {}).get("count"),
                    "Birthday": user.get("birthday"),
                    "Bio Links": [entity.get("hashtag", {}).get("name") for entity in user.get("biography_with_entities", {}).get("entities", []) if entity.get("hashtag")],
                    "Mutual Friends Count": user.get("edge_mutual_followed_by", {}).get("count"),
                    "Recent Stories": len(user.get("edge_felix_video_timeline", {}).get("edges", [])),
                    "Saved Collections": len(user.get("edge_saved_media", {}).get("edges", [])),
                    "Story Highlights Count": user.get("highlight_reel_count"),
                    "Pinned Posts Count": user.get("pinned_post_count"),
                    "Business Contact Info": user.get("business_contact_method"),
                    "Ad Preferences": user.get("ads_preferences"),
                    "Activity Log": user.get("activity_feed"),
                    "Shopping Behavior": user.get("shopping_tags"),
                }

                print("\n--- Profile Information ---")
                for key, value in profile_info.items():
                    print(f"{key}: {value if value else 'Could not find ' + key.lower().replace('_', ' ')}")

            except json.JSONDecodeError:
                logging.error("Failed to decode JSON response.")
            except AttributeError as e:
                logging.error("AttributeError: %s", e)
                logging.error("Data: %s", data)
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
