'''
Exercise 4 — Search for Books
● API: https://openlibrary.org/search.json?q=your+book+name
● Task: Ask the user to input a book title, send it as a query parameter, and print the top 5 results with title and author.
● Bonus: Handle the case where no results are found gracefully.
query = input("Enter a book title: ")
url = "https://openlibrary.org/search.json"
params = {"q": query}

'''

import requests

query = input("Enter a book title: ")

url = f"https://openlibrary.org/search.json?q={query}"

#or url = "https://openlibrary.org/search.json"
#params = {"q": query}
#response = requests.get(url, params=params)

response = requests.get(url) #gets a list of key-pair values
response_dic = response.json() 
book_details = response_dic['docs'] #details of books are in docs

if len(book_details)==0:
    print("No books found.")
else:
    for book in book_details[:5]:
        #book = book_details[book]

        print(f"Title of the book: {book['title']}")
        authors = book.get("author_name", ["Unknown Author"])
        print(f"Author: {authors[0]}")
        #print(f"Author: {book["author_name"][0]}")  #bc the author name is in list form, so printing the first(and only element in the list)
