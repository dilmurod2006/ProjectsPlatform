from requests import get, post



# login function
def login(api, username, password):
    return post(api, json={"username": username, "password": password})

api = "https://api.projectsplatform.uz/accounts/login"

response = login(api, "admin", "admin")

print(response.json()["detail"])