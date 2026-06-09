import os
from groq import Groq
from dotenv import load_dotenv

SYSTEM_PROMPT = """
You are a sharp, friendly assistant.
Give direct answers without unnecessary padding.
If you are uncertain, admit it instead of guessing.
Remember previous parts of the conversation.
"""


def load_model():

    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("ERROR: GROQ_API_KEY not found.")
        exit()

    try:
        client = Groq(
            api_key=api_key
        )

        return client

    except Exception:
        print("ERROR: Failed to initialize Groq.")
        exit()


def chat(client, history, message):

    history.append(
        {
            "role": "user",
            "content": message
        }
    )

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                *history
            ]
        )

        reply = response.choices[0].message.content.strip()

        history.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        return reply

    except Exception as e:

        history.pop()

        return f"Error: {e}"


def save_chat(history):

    with open(
        "chat_log.txt",
        "w",
        encoding="utf-8"
    ) as file:

        for message in history:

            if message["role"] == "user":

                file.write(
                    f"User: {message['content']}\n\n"
                )

            else:

                file.write(
                    f"Assistant: {message['content']}\n\n"
                )


def main():

    client = load_model()

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
            client,
            history,
            user_message
        )

        print(f"\nAI: {reply}")

        message_count += 1


if __name__ == "__main__":
    main()