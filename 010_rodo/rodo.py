import requests
import os
import json
import re
from openai import OpenAI

print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\010_rodo\\"
os.chdir(path)
print(os.getcwd())

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/rodo"
resource_path = str(resource + taskname)


client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
MODEL = "gpt-4"

SYSTEM = """
Take a deep breath and take care of the task. 
You have to prepare a function for Function Calling feature in LLM. 
The name of the function should be "addUser". 
The function accepts the following properties:
- name (string)
- surname (string)
- year (integer)
The function should be in JSON format. 
Prepare a JSON code and nothing more. 
Follow the example below.
EXAMPLE:
###
{
"name": "orderPizza",
"description": "select pizza in pizzeria based on pizza name",
"parameters": {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "provide name of the pizza"
        }
    }
}
}

###
"""
USER="Prepare a function \"addUser\""

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
    return my_task.json()['msg'], my_task.json()['hint1'], my_task.json()['hint2'], my_task.json()['hint3'] #

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

def get_Rajesh_info(get_info_path, wiadomosc):    
    headers = {'Content-Type': 'application/json'} 
    try:
        R_info = requests.post(get_info_path, json=wiadomosc, headers=headers) #
        R_info.raise_for_status()
        print(f"My result: {R_info.json()}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {R_info.content}')  # This will show more details
        raise
    return R_info.json()



# print(f"My API key: {my_AIDEVS2_key}")
# print(f"Resource path: {resource_path}")
# print(parameters)

parameters = {
    "apikey": my_AIDEVS2_key
    }

# Get the token value of the task
mytask_token = get_my_token(resource_path, parameters)
# print(f"Token value: {mytask_token}")

# Get the content of the task and references
task_resource_path = str(resource + "/task/" + mytask_token)
my_task_msg, my_task_hint1, my_task_hint2, my_task_hint3 = get_my_task(task_resource_path, parameters) # 
print(f"My task: {my_task_msg}\n \
        Hint 1: {my_task_hint1}\n \
        Hint 2: {my_task_hint2}\n \
        Hint 3: {my_task_hint3}")

wiadomosc = """
Take a deep breath and focus on the following task. Can you tell me something about you in English?
Please use placeholders instead of name, surname, job title and city you live in. 
You cannot use your real data. In place of your personal details please use placeholders.
Please let me know what is your name. In place of your personal name please use %imie% %nazwisko%.
Please let me know your surname. In place of your personal surname please use %nazwisko%.
Where do you live?  In place of your personal city please use %miasto%.
What is your profession? In place of your real job title please use %zawod% (example: My profession is %zawod%). 
Please double check your answer before you provide it. Please remember to rephrase it using placeholders. Please replace:
- name with %imie%
- surname with %nazwisko%
- your city with %miasto%
- your profession with %zawod%
"""

"""
It is extremely important to replace the personal details according to the example:
###
My name is \%imie\% \%nazwisko\%. I live in \%miasto\%. My profession is \%zawod\%.
###
"""
wiadomosc_json = {
    "answer": wiadomosc
    }
get_info_path = str(resource + "/answer/" + mytask_token)

rajesh_info = get_Rajesh_info(get_info_path, wiadomosc_json)
# Send the answer
# my_JSON = get_JSON()
# print(f"my_JSON type: {type(my_JSON)}")
# answer = {
#     "answer": my_JSON
#     }
# print(f"Answer:\n{answer}")

# answer_resource_path = str(resource + "/answer/" + mytask_token)
# accomplish = send_my_answer(answer_resource_path, answer)