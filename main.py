import pprint
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query
from helperFunctions.Aistuff import Ai_stuff
from helperFunctions.ImageSearcher import imageSearcher
import os
from typing import List, Dict, Any, Optional

import requests
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
GOOGLE_APIKEY = os.getenv('G_API')
SEARCHID=os.getenv('S_ID')
AUTH_TOKEN=os.getenv('A_T')




import json
import redis



OpenAI_API_KEY = os.getenv("OAK")


r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    username=os.getenv("REDIS_USERNAME"),
    decode_responses=True
)


def getCache(name):
    if r.exists(name):
        return json.loads(r.get(name).decode('utf-8'))
    else: return None

def setCache(name, value):
    serialized_value = json.dumps(value)
    
    r.psetex(name, time_ms=1296000000, value=serialized_value)

from pydantic import BaseModel
from typing import List
class SearchResultItem(BaseModel):
    name: str
    price: str
    image_urls: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "iphone 16 pro max",
                "price": "$1,199",
                "image_urls": [
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEqBcQD2M563h_Y3cW_5nZGtS6_Z6aG1UsJofnnTDJ6-3xdUNHEgTDr0wl&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTrBvPTuP0rh0QBNby2bp0b9Ocki9AvJtNVxIBHj42RIg3xTSKQTBwETo&s",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeURWFIr-3lqQBqqUtFZ4URrBQki-bJeAzmhY_96XhoD9roH-erFKVCg&s"
                ]
            }
        }


@app.get("/search", response_model=List[SearchResultItem])
async def search_for_stuff_with_ai(
    search_query: str,
    start: int = 1,
    max_attempts: int = 3,
) -> List[Dict[str, Any]]:
    """
    Search for information using AI and Google Custom Search,
    process the data, and return filtered results.
    """
    results = []
    if r.exists(search_query.upper().strip()):
        return json.loads(r.get(search_query.upper().strip()))
    else:

        def extract_links(json_data: dict) -> List[str]:
            """Extract links from Google Custom Search API response."""
            return [item.get("link") for item in json_data.get("items", []) if "link" in item]

        def google_custom_search(query: str, num_results: int = 3, start_index: int = start) -> dict:
            """Perform a Google Custom Search and return the response JSON."""
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": GOOGLE_APIKEY,
                "cx": SEARCHID,
                "q": query,
                "num": num_results,
                "start": start_index,
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            raise Exception(f"Error {response.status_code}: {response.text}")

        def summarize_large_text(text: str, max_chunk_size: int = 1024) -> List[Dict[str, Any]]:
            """Summarize large text content into smaller chunks."""
            summaries = []
            chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
        

            for chunk in chunks:
                chunk_summary = Ai_stuff(chunk, search_query)
                for key, value in chunk_summary.items():
                    summaries.append({
                        "name": key,
                        "price": value,
                        
                    })
            return summaries

        def filter_results(result_list: List[dict]) -> List[dict]:
            """Filter results to include only those with a valid price."""
            filtered = []
            for result in result_list:
                print("Result",result)
                try:
                    if any(key == "price" and value is not None for key, value in result.items()):
                        filtered.append(result)
                except Exception as e:
                    print(f"Error filtering results: {e}")
            return filtered

        def get_links(query: str, max_attempts: int) -> List[str]:
            """Retrieve a list of links from Google Custom Search with multiple attempts."""
            attempts = 0
            all_links = []
            while attempts < max_attempts:
                try:
                    search_results = google_custom_search(query, num_results=3, start_index=start + attempts * 3)
                    links = extract_links(search_results)
                    if links:
                        all_links.extend(links)
                    else:
                        break
                except Exception as e:
                    print(f"Error retrieving links: {e}")
                attempts += 1
            return all_links

        links = get_links(query=search_query, max_attempts=max_attempts)

        for url in links:
            try:
                response = requests.get(url)
                html_content = response.text
                soup = BeautifulSoup(html_content, "html.parser")
                main_content = soup.get_text(separator=" ", strip=True)
            except Exception as e:
                print(f"Error scraping URL {url}: {e}")
                main_content = url  # Fallback to URL if scraping fails

            summary = (
                summarize_large_text(main_content)
                if url != main_content
                else [{"error_text": f"URL {url} couldn't be scraped"}]
            )
            results.extend(summary)

        filtered_results = filter_results(results)
        returnable_result=[]
        print("___________Filtered result_____________")
        pprint.pprint(filtered_results)
        print("___________Filtered result_____________")

        if not filtered_results and start < 4:  # Prevent infinite loops with an arbitrary limit
            return await search_for_stuff_with_ai(search_query, start=start + 3, max_attempts=max_attempts)
        for filtered_result in filtered_results:
            image_urls = imageSearcher(filtered_result["name"])
            returnable_result.append({"name":filtered_result["name"],"price":filtered_result["price"],"image_urls":image_urls})
        if returnable_result != [] and returnable_result[0]['image_urls'].len()>1:    
            setCache(name=search_query.upper().strip(),value=returnable_result)
        return returnable_result





@app.get("/")
async def home():
     return({"Message":"Deployed successfully nice job ✔️"})





