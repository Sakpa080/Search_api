import os
import pprint
import requests
from dotenv import load_dotenv
load_dotenv()
GOOGLE_APIKEY = os.getenv('G_API')
SEARCHID=os.getenv('S_ID')
def google_custom_search( query, num_results=3, start=1):
        """
        Perform a custom Google search using Google Custom Search JSON API.
        
        Args:
            api_key (str): Your Google API key.
            cx (str): Your custom search engine ID.
            query (str): The search query.
            num_results (int): Number of results to fetch (default: 10, max: 10 per request).
            start (int): Starting index of search results (default: 1).

        Returns:
            dict: The search results.
        """
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_APIKEY,
            "cx": SEARCHID,
            "q": query,
            "num": num_results,
            "searchType":'image',
            "start": start,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
    

def imageSearcher(stuff):
    response = []
    try:
        for items in google_custom_search(stuff).get("items"):
            # pprint.pprint(items.get("image").get("thumbnailLink"))
            response.append(items.get("image").get("thumbnailLink"))
        return response
    except Exception as e:
         return response
        
