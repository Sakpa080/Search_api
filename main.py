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
OpenAI_API_KEY = os.getenv("OAK")

from openai import OpenAI
client = OpenAI(api_key=OpenAI_API_KEY)


# Define the initial messages array
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "I'm looking for someone to represent my brand help me write a search query for google to make it possible to find a brand ambassador my brand is of a pet care category and the business is based in london"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": " pet care brand ambassador London."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "I'm looking for someone to represent my brand help me write a search query for google to make it possible to find a brand ambassador my brand is of a pet care category and the business is based in Nigeria"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": " pet care brand ambassador Nigeria."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "I'm looking for someone to represent my brand help me write a search query for google to make it possible to find a brand ambassador my brand is of a Security Service category and the business is based in New york"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": " security service brand ambassador New York."
            }
        ]
    }
]



@st.cache_data(persist="disk")
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



st.selectbox(label="where is your brand based in?",options=[
    "Nigeria", "London", "New York", "Tokyo", "Paris", "Sydney", "Beijing", "Toronto", "Mumbai", "Dubai",
    "Berlin", "Cape Town", "Buenos Aires", "Moscow", "Cairo", "Seoul", "Bangkok", "Mexico City", "Jakarta", "Istanbul",
    "Rio de Janeiro", "Lagos", "Singapore", "Los Angeles", "Kuala Lumpur", "Rome", "Shanghai", "Melbourne", "Hong Kong", "Madrid",
    "Dublin", "Nairobi", "Lima", "Vienna", "Athens", "Manila", "Karachi", "Dhaka", "Abu Dhabi", "Amsterdam",
    "Chicago", "Bogotá", "Riyadh", "Santiago", "Barcelona", "Colombo", "Ankara", "Brisbane", "Kiev", "Warsaw",
    "San Francisco", "Doha", "Edinburgh", "Helsinki", "Oslo", "Stockholm", "Copenhagen", "Lisbon", "Vancouver", "Montreal",
    "Zurich", "Geneva", "Prague", "Budapest", "Brussels", "Hanoi", "Phnom Penh", "Kathmandu", "Islamabad", "Jakarta",
    "Canberra", "Addis Ababa", "Accra", "Casablanca", "Tunis", "Rabat", "Algiers", "Amman", "Tehran", "Baghdad",
    "Ho Chi Minh City", "Taipei", "Macau", "Perth", "Adelaide", "Darwin", "Christchurch", "Auckland", "Wellington", "Hobart",
    "Bangalore", "Hyderabad", "Pune", "Chennai", "Ahmedabad", "Surat", "Lucknow", "Patna", "Kolkata", "Jaipur"
]
,key="brand_location")
st.selectbox(label="What category or industry is your brand focused on?",options=[
    "Pet Care", "Security Services", "Luxury Shoes", "Bespoke Interior Designs", "Digital Marketing", "Fitness Coaching", 
    "Event Planning", "Handmade Jewelry", "Organic Farming", "Online Education", 
    "Photography Services", "Custom Furniture", "Tech Support", "Mobile App Development", "Virtual Assistant Services", 
    "Health and Wellness Products", "Eco-Friendly Packaging", "Financial Consulting", "Social Media Management", "Car Rental Services", 
    "Home Cleaning Services", "Landscaping", "Meal Prep Services", "Luxury Handbags", "Clothing Boutique", 
    "Graphic Design", "Tutoring Services", "Real Estate Development", "E-commerce Store", "Hair and Beauty Salon", 
    "Wedding Planning", "Drone Videography", "Food Truck", "Specialty Coffee", "Art Gallery", 
    "Catering Services", "Craft Supplies", "Mobile Car Wash", "Subscription Boxes", "Sustainable Fashion", 
    "IT Consulting", "Yoga Studio", "Auto Repair Shop", "Travel Agency", "Baking and Pastries", 
    "Bookstore", "Music Lessons", "Gift Wrapping Services", "Daycare Center", "Personal Training", 
    "Podcast Production", "Career Coaching", "Online Reselling", "Personal Styling", "Freelance Writing", 
    "Translation Services", "Gaming Lounge", "Interior Painting", "Renewable Energy Solutions", "Custom T-Shirts", 
    "Virtual Reality Experiences", "Public Relations Agency", "Coffee Roasting", "Candle Making", "Antique Restoration", 
    "Mobile Massage Therapy", "Life Coaching", "Childproofing Services", "Shoe Repair", "Toy Manufacturing", 
    "Pet Grooming", "Health Food Store", "Fishing Gear", "Gourmet Popcorn", "Customized Stationery", 
    "Self-Defense Classes", "Home Staging", "Party Supplies", "Computer Repair", "Sports Coaching", 
    "Mobile Notary Services", "Greenhouse Installation", "Car Detailing", "Solar Panel Installation", "Corporate Training", 
    "Video Editing Services", "Scented Soaps", "Woodworking", "Bed and Breakfast", "Sports Equipment Rental", 
    "Organic Skincare", "Wedding Photography", "Custom Cake Design", "Online Fitness Programs", "Property Management", 
    "SEO Services", "Virtual Event Hosting", "3D Printing Services", "Luxury Watches", "Tailoring and Alterations"
]
,key="brand_category")
st.text_input(label="What values or traits are most important to your brand when choosing an ambassador?(optional)",key="extra")
if st.button("Generate Search query"):
    new_user_input = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"I'm looking for someone to represent my brand help me write a search query for google to make it possible to find a brand ambassador my brand is of a {st.session_state.brand_category} category and the business is based in {st.session_state.brand_location} important values and traits to the brand--{st.session_state.extra}"
            }
        ]
    }

    # Append the new user input to the messages
    messages.append(new_user_input)

    # Make the API call
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:group-c::AgwZVJPq",
        messages=messages,
        response_format={
            "type": "text"
        },
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )   

    # Extract and print the assistant's response
    print(response.choices[0].message.content)
    assistant_response = response.choices[0].message.content
    st.session_state.search_query= assistant_response

st.text_input("what are you looking for ?",key="search_query",disabled=True)
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
                st.code(st.session_state.summaries[url].get('username'))
                st.image(image, caption=f"@{ st.session_state.summaries[url].get('username')}\'s Profile Picture ")
                st.link_button(type='secondary',label=f"Click me to go to @{st.session_state.summaries[url].get('username')}'s instagram page ",url=f"{st.session_state.summaries[url].get('profileLink')}")
                st.info(f"Bio: { st.session_state.summaries[url].get('biography')}",icon="🥇")
                st.code(st.session_state.summaries[url].get('username'))
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
st.markdown("[tap me to Go to the Top](#brand-ambassador-finder)")

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
