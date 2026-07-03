import math

def calculator(expression):
    try:
        allowed = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
    
def search(query):
    knowledge = {
        "population of pakistan": "Pakistan's population is approximately 240 million (2024).",
        "capital of france": "The capital of France is Paris.",
        "height of mount everest": "Mount Everest is 8,848.86 metres high.",
        "speed of light": "The speed of light is approximately 299,792,458 metres per second.",
        "pakistan independence": "Pakistan became independent on 14 August 1947.",
        "area of pakistan": "Pakistan covers approximately 881,913 square kilometres."
    }

    return knowledge.get(
        query.lower(),
        f"No result found for: {query}"
    )

print(calculator("17 * 38"))
print(calculator("144 ** 0.5"))

print(search("population of pakistan"))
print(search("capital of france"))
print(search("weather in tokyo"))