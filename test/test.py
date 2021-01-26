import requests
import json

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

p = {
    "userId": ["nani","joe","sdsd"],
    "name": ["df","Jogn"]
}
# response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
# response = requests.get('http://127.0.0.1:5000/api/users', params=p)
# jprint(response.json())
response = requests.get("http://127.0.0.1:5000/api/users")
jprint(response.json())
# # response = requests.post("http://127.0.0.1:5000/api/users?userId=abc123&name=The Rock&city=Los Angeles")
# response = requests.post("http://127.0.0.1:5000/api/users", data = {"userId":"abc123", "name": "The rock", "city": "LA"})
# jprint(response.json())
# response = requests.put("http://127.0.0.1:5000/api/users", data = {"userId":"abc123", "name": "The rock soft", "city": "LA"})
# jprint(response.json())
# response = requests.delete("http://127.0.0.1:5000/api/users", data = {"userId":"abc123", "name": "The rock", "city": "LA"})
# jprint(response.json())
# response = requests.get("http://127.0.0.1:5000/api/users")
# jprint(response.json())