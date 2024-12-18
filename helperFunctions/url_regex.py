import re

def extract_base_url(url):
    # Regex pattern to extract the base URL + username
    pattern = r'^(https:\/\/www\.instagram\.com\/[a-zA-Z0-9._]+)\/.*'
    
    # Match the URL using the regex pattern
    match = re.match(pattern, url)
    
    # If there's a match, return the base URL + username; otherwise, return None
    if match:
        return match.group(1)
    else:
        return None

