'''
Exercise 6 — POST Request Practice
    ● API: https://jsonplaceholder.typicode.com/posts
    ● Task: Send a POST request with a JSON body containing a title, body, and userId. Print the response.
    ● Note: This is a fake/mock API — great for safely practicing POST requests without any side effects.

'''

import requests

url = "https://jsonplaceholder.typicode.com/posts"

msg ={
    "title": "My first post",
    "body":"familiarization with APIs",
    "id":1

}

response = requests.post(url,json=msg)

print(response.status_code)
print(response.json())

