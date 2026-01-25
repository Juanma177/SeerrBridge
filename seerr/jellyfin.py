"""
Jellyfin integration module
Handles interaction with the Jellyfin API
"""
import requests
import time
from seerr.config import JELLYFIN_API_KEY, JELLYFIN_BASE_URL
from seerr.db_logger import log_info, log_error

def refresh_jellyfin_library() -> bool:
    """
    Trigger a library refresh in Jellyfin.
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not JELLYFIN_API_KEY or not JELLYFIN_BASE_URL:
        log_info("Jellyfin", "Jellyfin API Key or Base URL not set. Skipping library refresh.", module="jellyfin", function="refresh_jellyfin_library")
        return False

    # Remove trailing slash if present
    base_url = JELLYFIN_BASE_URL.rstrip('/')
    url = f"{base_url}/Library/Refresh"
    
    headers = {
        "X-MediaBrowser-Token": JELLYFIN_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        # Add a 15-second delay before triggering the refresh
        log_info("Jellyfin", "Waiting 15 seconds before refreshing Jellyfin library...", module="jellyfin", function="refresh_jellyfin_library")
        time.sleep(15)
        
        log_info("Jellyfin", "Attempting to refresh Jellyfin library...", module="jellyfin", function="refresh_jellyfin_library")
        # Send an empty POST request
        response = requests.post(url, headers=headers, data={})
        
        # Jellyfin returns 204 No Content on a successful trigger
        if response.status_code == 204:
            log_info("Jellyfin", "Successfully triggered Jellyfin library refresh.", module="jellyfin", function="refresh_jellyfin_library")
            return True
        else:
            log_error("Jellyfin Error", f"Failed to refresh Jellyfin library: Status code {response.status_code}, Response: {response.text}", module="jellyfin", function="refresh_jellyfin_library")
            return False
    except requests.exceptions.RequestException as e:
        log_error("Jellyfin Error", f"Error refreshing Jellyfin library: {str(e)}", module="jellyfin", function="refresh_jellyfin_library")
        return False