import requests

url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

querystring = {"term":"arrope"}

headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': "api_key"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(len(response.json()['list']))

print(response.json()['list'][0]['definition'].replace("[", "").replace("]", ""))
print(response.json()['list'][0]['example'].replace("[", "").replace("]", ""))