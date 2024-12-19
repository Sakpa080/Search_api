import pprint
from dotenv import load_dotenv
import os

load_dotenv()
APIFY_CLIENT_KEY = os.getenv('APIFY_API_KEY')
def instagram_scraping_function(instagramLink):
    from apify_client import ApifyClient

    try:
        # Initialize the ApifyClient with your API token
        client = ApifyClient(APIFY_CLIENT_KEY)

        # Prepare the Actor input
        run_input = {
            "directUrls": [f"{instagramLink}"],
            "resultsType": "details",
            "resultsLimit": 1,
            "searchType": "user",
            "searchLimit": 1,
            "addParentData": False,
        }

        # Run the Actor and wait for it to finish
        run = client.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)

        mainList = []

        # Fetch and print Actor results from the run's dataset (if there are any)
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            mainList.append(item)
            

        if not mainList:
            raise ValueError("No data returned from the scraping process.")

        response = {
            "profilePic": mainList[0].get('profilePicUrlHD', None) if mainList[0].get('profilePicUrlHD', None) is None else mainList[0].get('profilePicUrl', None),
            "biography": mainList[0].get('biography', None),
            "isVerified": mainList[0].get('verified', None),
            "username": mainList[0].get('username', None),
            "fullName": mainList[0].get('full_name', None) ,
            "No_of_followers": mainList[0].get("followersCount", None),
            "No_of_following": mainList[0].get("followsCount", None),
            "relatedProfiles": mainList[0].get('relatedProfiles', None),
            "main":mainList[0]
        }

        
        return response

    except KeyError as e:
        # Handle missing key in the response
        print(f"KeyError: {e}")
        return {"error": f"Missing key: {e}"}

    except ValueError as e:
        # Handle cases where no data is returned from scraping
        print(f"ValueError: {e}")
        return {"error": str(e)}

    except Exception as e:
        # Catch any other exceptions
        print(f"An error occurred: {e}")
        return {"error": "An unexpected error occurred."}
