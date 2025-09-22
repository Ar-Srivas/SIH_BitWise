from dotenv import load_dotenv
import os
from mistralai import Mistral
from fastapi import FastAPI
import serpapi
import re

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
async def search_chat(user_message: str):
    try:
        params = {
            "engine": "google",
            "q": user_message,
            "api_key": SERPAPI_API_KEY
        }
        search = serpapi.GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        return organic_results[:3] if organic_results else []
    except Exception as e:
        print(f"Search error: {e}")
        return []

def should_include_diagram(user_message: str, response_content: str = "") -> bool:
    """Determine if the response should include a diagram."""
    diagram_keywords = [
        'process', 'steps', 'workflow', 'procedure', 'method', 'approach',
        'plan', 'schedule', 'timeline', 'roadmap', 'path', 'journey',
        'structure', 'hierarchy', 'organization', 'relationship', 'connection',
        'flow', 'sequence', 'order', 'stage', 'phase', 'cycle', 'compare',
        'study', 'learn', 'decision', 'problem', 'solve'
    ]

    message_lower = user_message.lower()
    response_lower = response_content.lower()

    return any(keyword in message_lower or keyword in response_lower for keyword in diagram_keywords)

def generate_simple_flowchart(steps: list) -> str:
    """Generate a simple flowchart."""
    if len(steps) <= 1:
        return ""

    mermaid = "```mermaid\nflowchart TD\n"

    for i, step in enumerate(steps[:5]):
        step_id = chr(65 + i)
        clean_step = step.strip()[:40].replace('"', "'")

        if i == 0:
            mermaid += f'    {step_id}["{clean_step}"]\n'
        else:
            prev_id = chr(65 + i - 1)
            mermaid += f'    {prev_id} --> {step_id}["{clean_step}"]\n'

    mermaid += "```"
    return mermaid

def extract_steps_from_response(response: str) -> list:
    """Extract numbered steps or bullet points from the response."""
    numbered_pattern = r'^\d+\.\s*(.+)$'
    bullet_pattern = r'^[-*•]\s*(.+)$'

    steps = []
    lines = response.split('\n')

    for line in lines:
        line = line.strip()
        if re.match(numbered_pattern, line):
            step = re.match(numbered_pattern, line).group(1)
            steps.append(step)
        elif re.match(bullet_pattern, line):
            step = re.match(bullet_pattern, line).group(1)
            steps.append(step)

    return steps

async def send_chat(search_result, user_message):
    try:
        chat_res = client.chat.complete(
            model=model,
            messages=[
                {"role": "user",
                "content": f"""You are an expert counselor and have to guide students for their {user_message} and with the following current search : {search_result}
                            Answer to the point and be positive and motivating in your response. Do not mention the search in the answer.
                            If you are unable to find the answer then politely say that you are unable to find the answer.
                            Give some form of structured steps to achieve the students goal.
                            Keep the answer concise and under 200 words.
                            Structure your response with clear, numbered steps when providing guidance.
                            """}
            ]
        )

        response_content = chat_res.choices[0].message.content

        # Check if we should add a diagram
        if should_include_diagram(user_message, response_content):
            steps = extract_steps_from_response(response_content)

            if steps and len(steps) > 2:
                diagram = generate_simple_flowchart(steps)
                if diagram:
                    response_content = f"{diagram}\n\n{response_content}"

        return response_content

    except Exception as e:
        print(f"Mistral API error: {e}")
        return "I'm sorry, I'm having trouble processing your request right now. Please try again."