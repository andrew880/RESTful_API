import requests
import json

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

parameters = {
    "lat": 40.71,
    "lon": -74
}
# response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
response = requests.get("http://127.0.0.1:5000/api/Hello")
jprint(response.json())