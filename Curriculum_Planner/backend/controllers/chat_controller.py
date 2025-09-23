from dotenv import load_dotenv
import os
from mistralai import Mistral
import serpapi
import re
import base64
import zlib
import httpx

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
model = "ministral-3b-latest"

client = Mistral(api_key=MISTRAL_API_KEY)

KROKI_BASE_URL = "https://kroki.io"

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
    diagram_keywords = [
        "process", "steps", "workflow", "procedure", "method", "protocol",
        "plan", "roadmap", "framework", "blueprint", "algorithm",
        "flow", "sequence", "order", "stage", "phase", "pipeline",
        "timeline", "schedule", "milestone", "iteration", "cycle",
        "hierarchy", "structure", "organization", "system", "architecture",
        "learn", "teach", "explain", "study guide", "tutorial",
        "how to", "guide", "overview", "workflow", "process"
    ]

    message_lower = user_message.lower()
    response_lower = response_content.lower()

    has_keyword = any(keyword in message_lower or keyword in response_lower for keyword in diagram_keywords)
    print(f"Checking for diagram keywords: {has_keyword}")  # Debug log

    return has_keyword

def extract_code_from_model(text: str) -> str:
    text = text.strip()
    m = re.search(r'```(?:\w+\n)?(.*?)```', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r'@startuml.*?@enduml', text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(0).strip()
    m = re.search(r'(graph|sequenceDiagram|flowchart|classDiagram|stateDiagram|gantt|erDiagram|journey|pie|gitGraph)[\s\S]*', text, re.IGNORECASE)
    if m:
        return m.group(0).strip()
    return text.strip()

def detect_diagram_type(code: str) -> str:
    c = code.lower().strip()
    if "@startuml" in c or "skinparam" in c:
        return "plantuml"
    elif any(keyword in c for keyword in ["graph", "sequencediagram", "flowchart", "classdiagram", "statediagram", "gantt", "erdiagram"]):
        return "mermaid"
    elif "digraph" in c or c.startswith("graph"):
        return "graphviz"
    else:
        return "plantuml"

def encode_for_kroki(diagram_code: str) -> str:
    try:
        compressed = zlib.compress(diagram_code.encode("utf-8"), 9)
        return base64.urlsafe_b64encode(compressed).decode("ascii")
    except Exception as e:
        print(f"Encoding error: {e}")
        return ""

def analyze_diagram_content(user_message: str, response_content: str) -> str:
    message_lower = user_message.lower()
    response_lower = response_content.lower()
    combined = f"{message_lower} {response_lower}"
    if any(keyword in combined for keyword in ['timeline', 'schedule', 'roadmap', 'when', 'phases', 'stages', 'order', 'sequence']):
        return "timeline"
    elif any(keyword in combined for keyword in ['compare', 'vs', 'versus', 'difference', 'choice', 'options', 'alternatives', 'better']):
        return "comparison"
    elif any(keyword in combined for keyword in ['structure', 'hierarchy', 'organization', 'levels', 'categories', 'types', 'classification']):
        return "hierarchy"
    else:
        return "process"

async def generate_dynamic_diagram(user_message: str, response_content: str) -> str:
    try:
        content_type = analyze_diagram_content(user_message, response_content)

        # Create specific diagram prompt based on content type
        if content_type == "process":
            diagram_prompt = f"""Create a simple process flowchart for: {user_message}

Generate ONLY PlantUML code in this format:
@startuml
start
:Step 1: First action;
:Step 2: Second action;
:Step 3: Final action;
stop
@enduml

No explanations, just the code."""

        elif content_type == "timeline":
            diagram_prompt = f"""Create a timeline for: {user_message}

Generate ONLY PlantUML code in this format:
@startuml
!theme plain
robust "Timeline" as T
T is Idle
T@0 : Start
T@1 : Phase 1
T@2 : Phase 2
T@3 : Complete
@enduml

No explanations, just the code."""

        elif content_type == "hierarchy":
            diagram_prompt = f"""Create a hierarchy diagram for: {user_message}

Generate ONLY PlantUML code in this format:
@startuml
!theme plain
object "Main Topic" as main
object "Sub Topic 1" as sub1
object "Sub Topic 2" as sub2
main ||-- sub1
main ||-- sub2
@enduml

No explanations, just the code."""

        elif content_type == "comparison":
            diagram_prompt = f"""Create a comparison diagram for: {user_message}

Generate ONLY PlantUML code in this format:
@startuml
!theme plain
left to right direction
rectangle "Option A" as A
rectangle "Option B" as B
A <-> B : Compare
@enduml

No explanations, just the code."""

        else:  # default process
            diagram_prompt = f"""Create a simple flowchart for: {user_message}

Generate ONLY PlantUML code in this format:
@startuml
start
:Step 1;
:Step 2;
:Step 3;
stop
@enduml

No explanations, just the code."""

        print(f"Sending diagram prompt: {diagram_prompt[:100]}...")  # Debug log

        chat_res = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": diagram_prompt}]
        )

        raw_response = chat_res.choices[0].message.content.strip()
        print(f"Raw diagram response: {raw_response}")  # Debug log

        code = extract_code_from_model(raw_response)
        print(f"Extracted code: {code}")  # Debug log

        if not code or len(code) < 10:
            print("No valid diagram code extracted")
            return ""

        diagram_type = detect_diagram_type(code)
        print(f"Detected diagram type: {diagram_type}")  # Debug log

        # Try POST request to Kroki
        kroki_url = f"{KROKI_BASE_URL}/{diagram_type}/svg"

        async with httpx.AsyncClient(timeout=30.0) as http:
            try:
                resp = await http.post(
                    kroki_url,
                    content=code.encode("utf-8"),
                    headers={"Content-Type": "text/plain"}
                )

                print(f"Kroki POST response status: {resp.status_code}")  # Debug log

                if resp.status_code == 200:
                    svg_text = resp.text
                    # Check if response is actually SVG
                    if svg_text.strip().startswith('<svg'):
                        svg_b64 = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
                        print("Successfully generated diagram with POST")  # Debug log
                        return f'<div class="kroki-diagram dynamic-{content_type}"><img src="data:image/svg+xml;base64,{svg_b64}" alt="{content_type.title()} Diagram" style="max-width: 100%; height: auto;"/></div>'
                    else:
                        print(f"Invalid SVG response: {svg_text[:100]}")

            except Exception as post_error:
                print(f"POST request failed: {post_error}")

        # Fallback to GET request with encoding
        try:
            encoded = encode_for_kroki(code)
            if encoded:
                fallback_url = f"{KROKI_BASE_URL}/{diagram_type}/svg/{encoded}"
                print(f"Fallback URL: {fallback_url}")  # Debug log

                # Test the fallback URL
                async with httpx.AsyncClient(timeout=30.0) as http:
                    resp = await http.get(fallback_url)
                    print(f"Fallback response status: {resp.status_code}")

                    if resp.status_code == 200:
                        print("Successfully generated diagram with GET")  # Debug log
                        return f'<div class="kroki-diagram dynamic-{content_type}"><img src="{fallback_url}" alt="{content_type.title()} Diagram" style="max-width: 100%; height: auto;" onerror="this.style.display=\'none\'"/></div>'

        except Exception as fallback_error:
            print(f"Fallback failed: {fallback_error}")

        return ""  # Return empty if all methods fail

    except Exception as e:
        print(f"Dynamic diagram generation error: {e}")
        return ""

def extract_steps_from_response(response: str) -> list:
    steps = []
    lines = response.split("\n")
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+\.\s*(.+)$', line):
            step = re.match(r'^\d+\.\s*(.+)$', line).group(1)
            steps.append(step)
    return steps

async def send_chat(search_result, user_message):
    try:
        chat_res = client.chat.complete(
            model=model,
            messages=[{
                "role": "user",
                "content": f"""Answer this student question directly: {user_message}

Context (if relevant): {search_result}

RULES:
- Start immediately with the answer
- Be specific and actionable
- Use numbered steps for guidance
- Keep under 150 words
- Be encouraging but direct
- Don't mention searching or being an AI
- Avoid phrases like "I'd be happy to" or "Absolutely"

Example: "The study process involves 3 key steps: 1. Review materials..."
"""
            }]
        )

        response_content = chat_res.choices[0].message.content

        # Add diagram generation back
        if should_include_diagram(user_message, response_content):
            print(f"Generating diagram for: {user_message}")  # Debug log
            diagram_html = await generate_dynamic_diagram(user_message, response_content)
            if (diagram_html):
                print("Diagram generated successfully")  # Debug log
                response_content = f"{diagram_html}\n\n{response_content}"
            else:
                print("Diagram generation failed")  # Debug log

        return response_content

    except Exception as e:
        print(f"Chat error: {e}")
        return "I'm having trouble processing your request right now. Please try again."
