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


test_responses = [
    "Thought: I need to calculate this.\nAction: calculator\nInput: 17 * 38",

    "Thought: I have the answer.\nFinal Answer: The result is 646.",

    "I don't know what to do.",
]

for response in test_responses:
    print(f"Response: {repr(response)}")
    print(f"Parsed: {parse_response(response)}")
    print()