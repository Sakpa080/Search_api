from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query
from helperFunctions.instagram_scrape import instagram_scraping_function
from helperFunctions.url_regex import extract_base_url
import os
import requests
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
GOOGLE_APIKEY = os.getenv('G_API')
SEARCHID=os.getenv('S_ID')
AUTH_TOKEN=os.getenv('A_T')




@app.get("/getReport")
async def getReport(search_query):
    result =[]
    def extract_links(json_data):
        items = json_data.get("items", [])
        image_links = [item.get("link") for item in items if "link" in item]
        return image_links

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
            "start": start,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()  # JSON response containing the search results
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    for url in extract_links(google_custom_search(query=f"{search_query}")):
                try:
                    response = requests.get(url)
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    main_content = soup.get_text(separator=" ", strip=True)  
                except:
                     main_content=url
                    
              
                
                API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
                headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}

                def query(payload):
                    response = requests.post(API_URL, headers=headers, json=payload)
                    return response.json()

                def summarize_large_text(text, max_chunk_size=1024):
                    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
                    summaries = [query({"inputs": chunk,}) for chunk in chunks]
                    return summaries
                if url == main_content:
                     summary = [[{"summary_text":f"This url:{url} couldn't be scraped"}]]
                else:
                    summary = summarize_large_text(main_content)
                print("_________________________________________________________________________________")
                print(summary,url)
                result.append({f"summary_list":summary})
                print("_________________________________________________________________________________")
    return result 




@app.get("/getReportInstagram")
async def getReportInstgramSupport(search_query):
    result =[]
    def extract_links(json_data):
        items = json_data.get("items", [])
        image_links = [item.get("link") for item in items if "link" in item]
        return image_links

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
            "start": start,
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()  # JSON response containing the search results
            else:
                return (f"Error {response.status_code}: {response.text}")
        except Exception as e:
             return e
             

    for url in extract_links(google_custom_search(query=f"{search_query}")):
                print(url)
                try:
                    response = instagram_scraping_function(extract_base_url(url=url))
                    print(extract_base_url(url=url))
                    result.append(response)  
                    main_content=result
                except Exception as e:
                     print(e)
                     main_content=url
                    
              
                
                
                if url == main_content:
                     res = [[{"Error":f"This url:{url} couldn't be scraped"}]]
                     result.append(res)
               
                print("_________________________________________________________________________________")
              
                
                print("_________________________________________________________________________________")
    return result 





@app.get("/")
async def home():
     return({"Message":"deployed"})





