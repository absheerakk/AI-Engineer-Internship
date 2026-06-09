import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

SYSTEM_PROMPT = """
You are a sharp, friendly assistant.
Give direct answers without unnecessary padding.
If you are uncertain, admit it instead of guessing.
Remember previous parts of the conversation.
"""


def load_model():

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("ERROR: GEMINI_API_KEY not found.")
        exit()

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT
        )

        return model

    except Exception:
        print("ERROR: Failed to initialize Gemini.")
        exit()


def chat(model, history, message):

    history.append(
        {
            "role": "user",
            "parts": [message]
        }
    )

    try:

        response = model.generate_content(history)

        reply = response.text.strip()

        history.append(
            {
                "role": "model",
                "parts": [reply]
            }
        )

        return reply

    except ResourceExhausted:

        history.pop()

        return "Rate limit exceeded. Please wait and try again."

    except Exception as e:

        history.pop()

        return f"Error: {e}"


def save_chat(history):

    with open("chat_log.txt", "w", encoding="utf-8") as file:

        for message in history:

            if message["role"] == "user":
                file.write(
                    f"User: {message['parts'][0]}\n"
                )

            else:
                file.write(
                    f"Assistant: {message['parts'][0]}\n"
                )

            file.write("\n")


def main():

    model = load_model()

    history = []

    message_count = 0

    print("=" * 50)
    print("Welcome to Ask-The-AI")
    print("Type 'quit' to exit")
    print("Type '/clear' to clear memory")
    print("=" * 50)

    while True:

        user_message = input("\nYou: ").strip()

        if not user_message:
            continue

        if user_message.lower() == "/clear":

            history = []

            print("Conversation history cleared.")

            continue

        if user_message.lower() == "quit":

            save_chat(history)

            print(
                f"\nGoodbye! {message_count} messages exchanged."
            )

            break

        reply = chat(
            model,
            history,
            user_message
        )

        print(f"\nAI: {reply}")

        message_count += 1


if __name__ == "__main__":
    main()