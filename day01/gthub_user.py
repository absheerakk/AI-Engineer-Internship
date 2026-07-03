'''
    Exercise 5 — Get a GitHub User's Info
        ● API: https://api.github.com/users/{username}
        ● Task: Ask the user to input a GitHub username and display their name, bio, public repos count, and followers.
        ● Bonus: List their 5 most recent public repositories using https://api.github.com/users/{username}/repos.
        
        username = input("Enter a GitHub username: ")
        url = f"https://api.github.com/users/{username}"
'''

import requests
username = input("Enter a GitHub username: ")
url = f"https://api.github.com/users/{username}?sort=created&direction=desc"

response = requests.get(url)

user_details = response.json()

print("username: ", user_details['login'])
print("Bio: ",user_details['bio'])
print("public repos count: ",user_details['public_repos'])
print("Followers: ", user_details['public_repos'])

url_repos = f"https://api.github.com/users/{username}/repos"
repos = requests.get(url_repos)

repos_dic = repos.json()

for repo in repos_dic[:5]:
    print(f"Repository: {repo['name']}")
    print(f"URL: {repo['html_url']}")
    print()
