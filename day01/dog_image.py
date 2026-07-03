'''
    Exercise 3 — Fetch a Random Dog Image
        ● API: https://dog.ceo/api/breeds/image/random
        ● Task: Make a GET request and extract the image URL from the response. Print it.
        ● Bonus: Ask the user to input a breed name and fetch an image for that specific breed.
    # Bonus hint
    breed = input("Enter a breed: ").lower()
    url = f"https://dog.ceo/api/breed/{breed}/images/random"

'''

import requests

breed = input("Enter a breed: ").lower()
url = f"https://dog.ceo/api/breed/{breed}/images/random"

data = requests.get(url)
dog_img = data.json()
print(dog_img)