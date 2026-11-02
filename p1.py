# import json

# # Sample data
# data = {
#     "name": "Alice",
#     "age": 30,
#     "city": "New York"
# }

# # Convert to JSON
# json_data = json.dumps(data)
# print(json_data)

# status_code = {
#     200: "OK",
#     401: "Unauthorized",
#     404: "Not Found",
#     500: "Internal Server Error"
# }

import requests
r = requests.get('https://api.github.com/users/UH-ALI')
data = r.json()
print(data['login'], data['public_repos']) 

# how it's working:
# 1. The code imports the `requests` library, which is used to make HTTP requests in Python.
# 2. It sends a GET request to the GitHub API endpoint for the user "octocat".
# 3. The response from the API is stored in the variable `r`.
# 4. The status code of the response is printed.
# 5. The JSON data from the response is accessed and the "login" field is print