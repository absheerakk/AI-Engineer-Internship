'''
    Exercise 1 — Fetch a Random Joke
        ● API: https://official-joke-api.appspot.com/random_joke
        ● Task: Make a GET request and print the setup and punchline of the joke.
        ● Bonus: Loop it 5 times to get 5 different jokes.
'''

import requests
import json

url = 'https://official-joke-api.appspot.com/random_joke'

for i in range(5):
    joke_data = requests.get(url).text #get request to get the joke
    print(f"Joke {i+1}:")
    #print(type(joke_data)) -> currently string datatype

    # joke is now of string data type, even tho it appears to be a dictionary -> need to convert this into dictionary data 
    #this is bc if we need to parse and get/extract specfic data, like how we need only the setup and punchline of joke here,
    #we need the joke to be in dictinary form, or in json format.


    ''' 
    json.load() -	File → Python object
    *json.loads() -	String → Python object (here we use this to convert string to dictionary)
    json.dump()	-   Python object → File
    json.dumps() -	Python object → String
    '''
    joke_dict = json.loads(joke_data) 
    #print(type(joke_dict)) - its now dictionary type

    joke_setup = joke_dict['setup']
    joke_punchline = joke_dict['punchline']

    print("Setup of the Joke: ", joke_setup)
    print("Punchline of the joke: ",joke_punchline)

