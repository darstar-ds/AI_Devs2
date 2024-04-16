import requests
import os
import json
import re
import time
from openai import OpenAI

print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\011_scraper\\"
os.chdir(path)
print(os.getcwd())

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/scraper"
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
    return my_task.json()['msg'], my_task.json()['input'], my_task.json()['question'] #, my_task.json()['hint3']

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

def get_pizza_history(url):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
    # Get the text content of the response
        text_content = response.text
        print(f"Pizza history: {text_content}")
    elif response.status_code == 403:
        time.sleep(3)
        text_content = response.text
        print(f"Pizza history: {text_content}")
    elif response.status_code == 500:
        time.sleep(3)
        text_content = response.text
        print(f"Pizza history: {text_content}")
    else:
        print(f"Failed to retrieve content: Status code {response.status_code}")
    return text_content

def find_pizza_answer(pizza_history, my_task_question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": pizza_history},
            {"role": "user", "content": f"Odpowiedz na pytanie w maksymalnie 200 znakach. Pytanie: {my_task_question}"}
            ],
        temperature = 0
        )
    pizza_answer = response.choices[0].message.content
    
    return pizza_answer

parameters = {
    "apikey": my_AIDEVS2_key
    }

# print(f"My API key: {my_AIDEVS2_key}")
# print(f"Resource path: {resource_path}")
# print(parameters)

# Get the token value of the task
mytask_token = get_my_token(resource_path, parameters)
# print(f"Token value: {mytask_token}")

# Get the content of the task and references
task_resource_path = str(resource + "/task/" + mytask_token)
my_task_msg, my_task_input, my_task_question = get_my_task(task_resource_path, parameters) #, my_task_hint1, my_task_hint2, my_task_hint3
print(f"My task: {my_task_msg}\nInput: {my_task_input}\nQuestion: {my_task_question}") #

# Send the answer
pizza_history = get_pizza_history(my_task_input)
pizza_answer = str(find_pizza_answer(pizza_history, my_task_question))
print(f"Pizaa question: {my_task_question}\nPizza answer: {pizza_answer}\nLength: {len(pizza_answer)}")

answer = {
    "answer": pizza_answer
    }

answer_resource_path = str(resource + "/answer/" + mytask_token)
accomplish = send_my_answer(answer_resource_path, answer)