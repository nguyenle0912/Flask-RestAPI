import requests
import secrets
BASE = "http://127.0.0.1:5000/"

#an array of jsons for creation of multiple tags via post if wanted
linux_data = {"name": "linux",
        "contents": "I'd just like to interject for a moment. What you're referring to as Linux is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux..."}


print("\nMake a POST request for the linux tag...")
post_url = BASE + "tags/linux"
print("Calling POST", post_url)
response = requests.post(post_url, linux_data) #first tag is linux
print(response.json())

print("\nMake a GET request for the linux tag after its creation...")
get_url = BASE + "tags/linux"
print("Calling GET", get_url)
response = requests.get(get_url)
print(response.json())

update_data = { "contents": "Something else" }
print("\nMake a PATCH request to update the linux tag...")
patch_token = input("\tEnter the token of the tag you want to update: ")
patch_url = BASE + "tags/linux/" + patch_token
print("\tCalling PATCH", patch_url)
response = requests.patch(patch_url, update_data)
print(response.json())

print("\nMake a GET request for the linux tag after its update...")
get_url = BASE + "tags/linux"
print("\tCalling GET", get_url)
response = requests.get(get_url)
print(response.json())

print("\nMake a DELETE request to delete the linux tag...")
delete_token = input("\tEnter the token of the tag you want to delete: ")
delete_url = BASE + "tags/linux/" + delete_token
print("\tCalling DELETE", delete_url)
response = requests.delete(delete_url)
print(response.json())

print("\nMake a GET request for the linux tag after delete...")
get_url = BASE + "tags/linux"
print("\tCalling GET", get_url)
response = requests.get(get_url)
print(response.json())

# for i in range(len(data)):
#     #generate token for each data
#     post_url = BASE + "tags/" + data[i]["name"]
#     print("Calling POST", post_url)
#     response = requests.post(post_url, data[i]) #first tag is linux
#     print(response.json())
