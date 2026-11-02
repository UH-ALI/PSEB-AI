# Task 1: API (GitHub)
# - Use the GitHub API to fetch details of 3 usernames of your choice.
# - Display each user's login and public repository count.
# - Verify that the API response status code is 200 before processing the data.

import requests
r = requests.get('https://api.github.com/users/UH-ALI')
if r.status_code == 200:
    data = r.json()
    print(data['login'], data['public_repos'])
else:
    print("Error: Failed to fetch data from GitHub API")
    print(r.status_code)

r1 = requests.get('https://api.github.com/users/Raysh454')
if r1.status_code == 200:
    data1 = r1.json()
    print(data1['login'], data1['public_repos'])    
else:
    print("Error: Failed to fetch data from GitHub API")
    print(r1.status_code)

r2 = requests.get('https://api.github.com/users/huzpro')
if r2.status_code == 200:
    data2 = r2.json()
    print(data2['login'], data2['public_repos'])
else:
    print("Error: Failed to fetch data from GitHub API")
    print(r2.status_code)
