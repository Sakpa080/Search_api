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

OpenAI_API_KEY = os.getenv("OAK")





@app.get("/search")
async def search_For_Stuff_With_Ai(
    search_query: str,
    start: int = 1,
    max_attempts: int = 5,
) -> List[Dict[str, Any]]:
    result = []

    def extract_links(json_data):
        items = json_data.get("items", [])
        return [item.get("link") for item in items if "link" in item]

    def google_custom_search(query, num_results=3, start=start):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_APIKEY,
            "cx": SEARCHID,
            "q": query,
            "num": num_results,
            "start": start,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")
    img_urls = imageSearcher(f"Logo of {search_query}") or []

    def summarize_large_text(text, max_chunk_size=1024):
        chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
        summaries = [Ai_stuff(chunk, search_query) for chunk in chunks]
        
        for summary in summaries:
            for key, value in summary.items():
                summary[key] = {"price": value, "image_urls": img_urls}
        return summaries

    def filter_results(resultlist):
        filtered_results = []
        for results in resultlist:
            for result in results:
                try:
                    for key, value in result.items():
                        if value.get("price") is not None:
                            filtered_results.append(result)
                            break
                except Exception as e:
                    print(f"Error filtering results: {e}")
        return filtered_results

    def get_links(query, max_attempts):
        attempts = 0
        all_links = []
        while attempts < max_attempts:
            try:
                search_results = google_custom_search(query, num_results=3, start=start + attempts * 3)
                links = extract_links(search_results)
                if links:
                    all_links.extend(links)
                else:
                    break
            except Exception as e:
                print(f"Error in link retrieval: {e}")
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
            main_content = url  # Use URL as fallback content

        summary = (
            summarize_large_text(main_content)
            if url != main_content
            else [[{"error_text": f"URL {url} couldn't be scraped"}]]
        )
        result.append(summary)

    filtered_results = filter_results(result)
    print(filtered_results,start)

    if not filtered_results and start < 100:  # Arbitrary limit to prevent infinite loops
        return await search_For_Stuff_With_Ai(search_query, start=start + 3, max_attempts=max_attempts)

    return filtered_results





@app.get("/")
async def home():
     return({"Message":"Deployed successfully nice job ✔️"})





