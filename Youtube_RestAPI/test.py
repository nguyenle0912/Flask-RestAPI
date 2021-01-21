import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name": "My First Video", "views": 10000, "likes": 10},
        {"name": "My second video", "views": 20000, "likes": 50},
        {"name": "How to make REST API in Python", "views": 30000, "likes": 100}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()

for i in range(len(data)):
    response = requests.get(BASE + "video/" + str(i))
    print(response.json())

input()

response = requests.delete(BASE + "video/0")
print(response)

for i in range(len(data)):
    response = requests.get(BASE + "video/" + str(i))
    print(response.json())

