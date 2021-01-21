import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name": "My First Video", "views": 10000, "likes": 10},
        {"name": "My second video", "views": 20000, "likes": 50},
        {"name": "How to make REST API in Python", "views": 30000, "likes": 100}]

response = requests.patch(BASE + "video/2", {"name": "Tim", "views": 100, "likes": 35})
print(response.json())

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())

input()
response = requests.get(BASE + "video/2")
print(response.json())

