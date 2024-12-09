import requests

url = "http://18.221.248.193/fact"

#test the facts
headers = {
    "Amount": "10"
}
response = requests.get(url, headers=headers)
print(response.text)

#test the info
url = "http://18.221.248.193/info"
response = requests.get(url)
print(response.text)
