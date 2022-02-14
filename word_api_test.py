import requests

url = "https://twinword-word-graph-dictionary.p.rapidapi.com/definition/"

querystring = {"entry":"mask"}

headers = {
    'x-rapidapi-host': "twinword-word-graph-dictionary.p.rapidapi.com",
    'x-rapidapi-key': "your_api"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.json()['meaning']['noun'])