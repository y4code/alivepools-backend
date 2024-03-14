import requests

def check_website_availability(website):
    if not website.startswith(("http://", "https://")):
        website = "http://" + website
    try:
        for _ in range(5):
            response = requests.get(website)
            if response.status_code == 200:
                return True
    except requests.exceptions.RequestException:
        return False