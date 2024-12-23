from openai import OpenAI
import json
import os
from dotenv import load_dotenv
load_dotenv()
OpenAI_API_KEY = os.getenv("OAK")
client = OpenAI(OpenAI_API_KEY)


def Ai_stuff(content,item_name):
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "You are a website scraper that scrape's the price's of things of a websites content \nreturn a json object if content contains the right information else return \"None\"\n\"name of item\": \"price of item\"\n"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What is the price of a  ' 2024 Lamborghini ' if the information is below return it else if the information isn't below return 'None' \n\nCars\nSedans, coupes, convertibles, and wagons\n2024 Lamborghini Huracán\n9.5\n/10\nC/D RATING\nStarting at\n$249,865\nEPA MPG\n15 combined\nC/D SAYS: The 2024 Huracán excels at everything important except being subtle, which makes it an ideal supercar and the perfect Lamborghini. Learn More\nEXPAND ALL MODEL YEARS\nLamborghini Huracán Model Years\nView 2024 Huracán Details\nStarting at $249,865 · 9.5/10\nView 2023 Huracán Details\nStarting at $212,090 · 9.5/10\nView 2022 Huracán Details\nStarting at $213,104 · 9.5/10\nView 2021 Huracán Details\nStarting at $214,866 · 9.5/10\nView 2020 Huracán Details\nStarting at $212,266 · 9.5/10\nView 2019 Huracán Details\nStarting at $209,469 · 10/10\nCOLLAPSE\n2025 Lamborghini Revuelto\n10\n/10\nC/D RATING\nStarting at\n$609,000 est\nEPA MPG\nN/A\nC/D SAYS: The Revuelto stays true to Lamborghini's 12-cylinder spirit while using hybrid tech to push past internal-combustion limitations. Learn More\nEXPAND ALL MODEL YEARS"
            }
        ]
        },
        {
        "role": "assistant",
        "content": [
            {
            "type": "text",
            "text": "{\n  \"2024 Lamborghini Huracán\": \"$249,865\"\n}"
            }
        ]
        }
    ]
    new_user_input = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"What is the price of a  ' {item_name} ' if the information is below return it else if the information isn't below return 'None' {content}"
            }
        ]
    }
    messages.append(new_user_input)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=messages,
    response_format={
        "type": "json_object"
    },
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    
    assistant_response = response.choices[0].message.content
    return json.loads(assistant_response)
