import streamlit as st
from io import BytesIO
from PIL import Image
import os
import requests
from dotenv import load_dotenv
load_dotenv()
GOOGLE_APIKEY = os.getenv('G_API')
SEARCHID=os.getenv('S_ID')
BASE_URL = os.getenv('BASE_URL')



def get_report(search_query):
    # Define the base URL (this should be the server or API endpoint you're hitting)
    request_url =f"{BASE_URL}/getReportInstagram" 
    
    # Define the query parameter
    params = {
        'search_query': search_query
    }
    
    # Perform the GET request
    response = requests.get(request_url, params=params)
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        st.session_state.summaries = data
        for images in st.session_state.summaries:
                st.session_state.images.append(images.get("profilePic"))
                st.session_state.userNames.append(images.get("username"))

    else:
        st.session_state.images=[]
        st.session_state.summaries=None




if "images" not in st.session_state:
    st.session_state.images=[]

if "summaries" not in st.session_state:
    st.session_state.summaries=None

if "userNames" not in st.session_state:
    st.session_state.userNames=[]

def extract_image_links(json_data):
    items = json_data.get("items", [])
    image_links = [item.get("link") for item in items if "link" in item]
    return image_links


def search_func():
    st.session_state.images = []
    st.session_state.userNames=[]
    if st.session_state.search_query:
        with st.spinner(text="Loading Summary...",_cache=True):
            get_report(search_query=st.session_state.search_query)
            
            
        # Print results
        
        print("searching...")
    else:
        st.info("Nothing is in the search bar")
    print("Clicked!")

st.set_page_config(page_title="Ambassador Search engine with AI",page_icon="👾")
st.write("# Brand Ambassador Finder")
st.text_input("what are you looking for ?",key="search_query")
st.button("Search",on_click=search_func)
if st.session_state.images:
    tabs = st.tabs(st.session_state.userNames)
    for url,tab in enumerate(tabs):
         
    # Fetch image from the URL
        try:
            response = requests.get(st.session_state.images[url])
            image = Image.open(BytesIO(response.content))
            # Display image
            with tab:
                st.image(image, caption=f"@{ st.session_state.summaries[url].get('username')}\'s Profile Picture ")
                st.link_button(type='secondary',label=f"Click me to go to @{st.session_state.summaries[url].get('username')}'s instagram page ",url=f"{st.session_state.summaries[url].get('profileLink')}")
                st.info(f"Bio: { st.session_state.summaries[url].get('biography')}",icon="🥇")
                st.write(f"Full Name :red-background[{ st.session_state.summaries[url].get('fullName')}]")
                st.write(f"Username @:blue-background[{ st.session_state.summaries[url].get('username')}]")
                st.write(f"Number of People Following @{st.session_state.summaries[url].get('username')} :green-background[{ st.session_state.summaries[url].get('No_of_followers')}]")
                st.write(f"Number of people @{st.session_state.summaries[url].get('username')} follows: :blue-background[{ st.session_state.summaries[url].get('No_of_following')}]")
                st.write(f"### :rainbow-background[Related Profiles]")
                st.divider()
                st.write(st.session_state.summaries[url].get("relatedProfiles"))
                st.divider()
                
        except Exception as e:
            
            if str(e)=="bad argument type for built-in operation":
                pass
            else:
                st.warning(f"something went wrong {e}")
st.markdown("[Go to Top Button](#brand-ambassador-finder)")

st.markdown('''
    <style>
        /* Style for the back-to-top button */
        .back-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #ffffff;
            color: white;
            border: none;
            border-radius: 100%;
            padding: 25px;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            z-index: 100;
        }

        .back-to-top:hover {
            background-color: #499CD7;
        }

    </style>

    <!-- Button that will scroll the page back to the top -->
    <a href="#brand-ambassador-finder" class="back-to-top" id="back-to-top-button">
        👆🏿
    </a>

    <!-- Anchor at the top of the page to scroll to -->
    <a name="top"></a>
''', unsafe_allow_html=True)
