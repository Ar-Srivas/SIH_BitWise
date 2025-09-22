from dotenv import load_dotenv
import os
from mistralai import Mistral
from fastapi import FastAPI
import serpapi
from openai import OpenAI


'''
Logic 1 is user message goes to search then llm then send the answer

Logic 2 is input llm search llm answer

doing logic 1
'''
# Load environment variables
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
# OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
model = "mistral-large-latest"

client = Mistral(api_key=MISTRAL_API_KEY)

# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=OPENROUTER_API_KEY,
# )

# SerpApi search
async def search_chat(user_message:str):
    params = {
    "engine": "google",
    "q": user_message,
    "api_key": SERPAPI_API_KEY
    }
    search = serpapi.GoogleSearch(params)
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
                        Do not use markdown format
                        Do not include any emojis and make it formal.
                        Keep the answer concise on fluff and more on the data.
                        Restrict your answers down to 500 to 600 words.
                        """}
        ]
    )
    return chat_res.choices[0].message.content
#print(organic_results)    #CRAZY OUTPUT HAI ISKA

# async def send_chat(search_result, user_message):
#     completion = client.chat.completions.create(
#     model="openai/gpt-4o",
#     messages=[
#         {"role": "user",
#             "content": f"""You are a expert counselor and have to guide students for their {user_message} and with the following current search : {search_result}
#                         Answer to the point and be postive and motivating in your response. Do not mention the search in the answer.
#                         If you are unable to find the answer then politely say that you are unable to find the answer.
#                         Give some form of structured steps to achieve the stuedents goal.
#                         Do not use markdown format
#                         Do not include any emojis and make it formal.
#                         Keep the answer concise on fluff and more on the data.
#                         """}
#             ]
#             )
#     print(completion.choices[0].message.content)
