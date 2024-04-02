import requests
import os

my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/helloapi"
resource_path = str(resource + taskname)

# resource_path = 'https://tasks.aidevs.pl/token/helloapi'

def get_my_token(resource_path, parameters):
    headers = {'Content-Type': 'application/json'} 
    try:
        my_token = requests.post(resource_path, json=parameters, headers=headers)
        my_token.raise_for_status()
        print(f"My token: {my_token}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {my_token.content}')  # This will show more details
        raise
    return my_token.json()['token']

def get_my_task(task_resource_path, parameters):
    headers = {'Content-Type': 'application/json'} 
    try:
        my_task = requests.get(task_resource_path, json=parameters, headers=headers)
        my_task.raise_for_status()
        print(f"My task: {my_task.json()}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {my_task.content}')  # This will show more details
        raise
    return my_task.json()['msg'], my_task.json()['cookie']

def send_my_answer(resource_path, answer):
    headers = {'Content-Type': 'application/json'} 
    try:
        my_answer = requests.post(resource_path, json=answer, headers=headers)
        my_answer.raise_for_status()
        print(f"My result: {my_answer.json()}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {my_answer.content}')  # This will show more details
        raise
    return my_answer.json()

parameters = {
    "apikey": my_AIDEVS2_key
    }

print(f"My API key: {my_AIDEVS2_key}")
print(f"Resource path: {resource_path}")
print(parameters)
helloapi_token = get_my_token(resource_path, parameters)
print(f"Token value: {helloapi_token}")

task_resource_path = str(resource + "/task/" + helloapi_token)
my_task_msg, my_task_cookie = get_my_task(task_resource_path, parameters)
print(f"Message: {my_task_msg} \nCookie: {my_task_cookie}")

answer = {
    "answer": my_task_cookie
    }

answer_resource_path = str(resource + "/answer/" + helloapi_token)
accomplish = send_my_answer(answer_resource_path, answer)