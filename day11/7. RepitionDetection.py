import os
import math
import re
import time
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------------
# Gemini Setup
# -------------------------------

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def calculator(expression):
    try:
        allowed = {
            name: getattr(math, name)
            for name in dir(math)
            if not name.startswith("_")
        }

        result = eval(
            expression,
            {"__builtins__": {}},
            allowed,
        )

        return str(result)

    except Exception as e:
        return f"Error: {e}"

import requests

def search(query):
    topic = query.strip().replace(" ", "_")

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "PythonAgent/1.0"}
        )

        if response.status_code != 200:
            return f"No Wikipedia article found for: {query}"

        data = response.json()

        if "extract" in data:
            return data["extract"]

        return f"No Wikipedia article found for: {query}"

    except requests.exceptions.RequestException as e:
        return f"Search error: {e}"
    

def convert(expression):
    expression = expression.lower().replace("degrees", "").strip()
    parts = expression.split()

    if len(parts) != 4 or parts[2] != "to":
        return f"No conversion found for: {expression}"

    try:
        value = float(parts[0])
    except ValueError:
        return f"No conversion found for: {expression}"

    aliases = {
        "km": "km",
        "kilometre": "km",
        "kilometres": "km",
        "kilometer": "km",
        "kilometers": "km",

        "mile": "miles",
        "miles": "miles",

        "kg": "kg",
        "kilogram": "kg",
        "kilograms": "kg",

        "lb": "lbs",
        "lbs": "lbs",
        "pound": "lbs",
        "pounds": "lbs",

        "c": "celsius",
        "celsius": "celsius",

        "f": "fahrenheit",
        "fahrenheit": "fahrenheit",
    }

    from_unit = aliases.get(parts[1])
    to_unit = aliases.get(parts[3])

    if from_unit is None or to_unit is None:
        return f"No conversion found for: {expression}"

    if from_unit == "km" and to_unit == "miles":
        result = value * 0.621371
        return f"{value:g} km = {result:.3f} miles"

    elif from_unit == "miles" and to_unit == "km":
        result = value / 0.621371
        return f"{value:g} miles = {result:.3f} km"

    elif from_unit == "kg" and to_unit == "lbs":
        result = value * 2.20462
        return f"{value:g} kg = {result:.3f} lbs"

    elif from_unit == "lbs" and to_unit == "kg":
        result = value / 2.20462
        return f"{value:g} lbs = {result:.3f} kg"

    elif from_unit == "celsius" and to_unit == "fahrenheit":
        result = (value * 9 / 5) + 32
        return f"{value:g} Celsius = {result:.1f} Fahrenheit"

    elif from_unit == "fahrenheit" and to_unit == "celsius":
        result = (value - 32) * 5 / 9
        return f"{value:g} Fahrenheit = {result:.1f} Celsius"

    return f"No conversion found for: {expression}"

TOOLS = {
    "calculator": calculator,
    "search": search,
    "convert" : convert
}

SYSTEM_PROMPT = """

You are an AI agent that can use tools.

You have access to these tools:

calculator
- Evaluates mathematical expressions.
Example Input:
17 * 38
sqrt(144)

search
- Searches Wikipedia. Input must be a short topic or article title, NOT a full
  question. Strip the question down to its core subject before searching.
Example Input:
telephone
population of Pakistan

Good: "telephone", "Alexander Graham Bell"
Bad: "who invented the telephone", "when was the telephone invented"

convert: 
- Converts between common units.
Example Input: a conversion expression, e.g. "5 km to miles" or "100 celsius to fahrenheit"

If a search returns "No result found", do NOT retry the same question with
different phrasing. Searching twice for the same fact is enough — if both
attempts fail, give a Final Answer immediately saying the information could
not be found. Do not rephrase and search a third time.

You must ALWAYS start your response with a "Thought:" line explaining your
reasoning, before any Action or Final Answer. Never skip the Thought line.

When you need a tool, respond ONLY in this format, and ALWAYS include the Thought line:

Thought: <reasoning>
Action: <tool name>
Input: <tool input>

Call ONLY ONE tool at a time.

After receiving an Observation, continue reasoning.

When you know the answer, respond ONLY in this format:

Thought: <reasoning>
Final Answer: <answer>

Never guess numbers.
Always use the calculator.

Always use tools for calculations, facts, and conversions. Never guess at numbers.
"""

def parse_response(text):
    lines = text.splitlines()
    action = None
    tool_input = None

    for line in lines:
        if line.startswith("Action:"):
            action = line.replace("Action:", "").strip()
        elif line.startswith("Input:"):
            tool_input = line.replace("Input:", "").strip()
        elif line.startswith("Final Answer:"):
            answer = line.replace("Final Answer:", "").strip()
            return ("final", answer)

    if action and tool_input:
        return ("tool", action, tool_input)

    return ("final", text)


def run_agent(question, max_steps=6):

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT,
        generation_config=genai.types.GenerationConfig(
            stop_sequences=["Observation:"]
        ),
    )

    history = [
        {
            "role": "user",
            "parts": [question]
        }
    ]

    # Removed the extra newlines here to match the output spacing
    print(f"Question: {question}")
    
    past_calls = set()

    for step in range(1, max_steps + 1):

        response = model.generate_content(history)
        reply = response.text.strip()
        time.sleep(13) 
        
        print(f"--- Step {step} ---")
        print(reply)

        parsed = parse_response(reply)

        # Final Answer
        if parsed[0] == "final":
            answer = parsed[1]
            return answer

        # Tool Call
        _, tool_name, tool_input = parsed
        
        tool = TOOLS.get(tool_name)

        if tool is None:
            print(f"Unknown tool: {tool_name}")
            return

        observation = tool(tool_input)

        # Removed extra newlines here as well
        print(f"[Tool: {tool_name}('{tool_input}')]")
        print(f"[Observation: {observation}]")

        # --- REPETITION DETECTION GUARD ---
        current_tool_call = (tool_name, tool_input)
        if current_tool_call in past_calls:
            msg = f"Agent stuck: repeated call to {tool_name}('{tool_input}'). Stopping."
            print(msg)
            return msg
        past_calls.add(current_tool_call)
        # ----------------------------------

        # Save model reply
        history.append(
            {
                "role": "model",
                "parts": [reply]
            }
        )

        # Send observation back
        history.append(
            {
                "role": "user",
                "parts": [f"Observation: {observation}"]
            }
        )

    print("Step limit reached.")
    return "Step limit reached."


run_agent("What is the population of the city of Zibbleforth?")