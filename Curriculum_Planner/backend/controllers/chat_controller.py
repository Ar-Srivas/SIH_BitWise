from dotenv import load_dotenv
import os
from mistralai import Mistral
from fastapi import FastAPI
from serpapi import GoogleSearch



'''
Logic 1 is user message goes to search then llm then send the answer

Logic 2 is input llm search llm answer

doing logic 1
'''
# Load environment variables
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
model = "mistral-large-latest"

client = Mistral(api_key=MISTRAL_API_KEY)

# SerpApi search
async def search_chat(user_message:str):
    params = {
    "engine": "google",
    "q": "Best colleges for computer science MUMBAI",
    "api_key": SERPAPI_API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results")
    return organic_results



async def send_chat(search_result, user_message):
    chat_res = client.chat.complete(
        model=model,
        messages=[
            {"role": "user",
            "content": f"""You are a expert counselor and have to guide students for their {user_message} and with the following current search : {search_result}
                        Answer to the point and be postive and motivating in your response. Do not mention the search in the answer.
                        If you are unable to find the answer then politely say that you are unable to find the answer.
                        Give some form of structured steps to achieve the stuedents goal.
                        """}
        ]
    )
    return chat_res
#print(organic_results)    #CRAZY OUTPUT HAI ISKA
