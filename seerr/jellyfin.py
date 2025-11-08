"""
Jellyfin integration module
Handles interaction with the Jellyfin API
"""
import requests
import time  # Import the time module
from loguru import logger

from seerr.config import JELLYFIN_API_KEY, JELLYFIN_BASE_URL

def refresh_jellyfin_library() -> bool:
    """
    Trigger a library refresh in Jellyfin.
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not JELLYFIN_API_KEY or not JELLYFIN_BASE_URL:
        logger.info("Jellyfin API Key or Base URL not set. Skipping library refresh.")
        return False

    url = f"{JELLYFIN_BASE_URL}/Library/Refresh"
    headers = {
        "X-MediaBrowser-Token": JELLYFIN_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        # Add a 15-second delay before triggering the refresh
        logger.info("Waiting 15 seconds before refreshing Jellyfin library...")
        time.sleep(15)
        
        logger.info("Attempting to refresh Jellyfin library...")
        # Send an empty POST request
        response = requests.post(url, headers=headers, data={})
        
        # Jellyfin returns 204 No Content on a successful trigger
        if response.status_code == 204:
            logger.info("Successfully triggered Jellyfin library refresh.")
            return True
        else:
            logger.error(f"Failed to refresh Jellyfin library: Status code {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Error refreshing Jellyfin library: {str(e)}")
        return False