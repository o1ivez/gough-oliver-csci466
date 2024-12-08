import requests

url = "http://3.145.36.234/fact"

#test the facts
headers = {
    "Amount": "10"
}
response = requests.get(url, headers=headers)
print(response.text)

#test the info
url = "http://3.145.36.234/info"
response = requests.get(url)
print(response.text)
