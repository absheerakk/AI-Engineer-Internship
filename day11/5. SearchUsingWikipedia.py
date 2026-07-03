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
    

print("Pakistan:")
print(search("Pakistan"))
print()

print("France:")
print(search("France"))
print()

print(search("mkkmkjbhbjk"))