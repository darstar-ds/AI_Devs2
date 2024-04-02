import requests
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
MODEL = "gpt-4"

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/liar"
resource_path = str(resource + taskname)

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
    return my_task.json()['msg'], my_task.json()['hint1'], my_task.json()['hint2'], my_task.json()['hint3']

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

def get_answer_2_question(my_question, my_task_token):
    tricky_answer_path = str(resource + "/task/" + my_task_token)
    tricky_answer = requests.post(tricky_answer_path, data=my_question)
    print(f"Tricky answer: {tricky_answer.json()}")
    print(type(tricky_answer))
    tricky_answer_json = tricky_answer.json()
    print(tricky_answer_json["answer"])
    if "Warsaw" in tricky_answer_json["answer"]:
        return "YES"
    else: 
        return "NO"

parameters = {
    "apikey": my_AIDEVS2_key
    }

# print(f"My API key: {my_AIDEVS2_key}")
# print(f"Resource path: {resource_path}")
# print(parameters)

# Get the token value of the task
mytask_token = get_my_token(resource_path, parameters)
print(f"Token value: {mytask_token}")

# Get the content of the task and references
task_resource_path = str(resource + "/task/" + mytask_token)
my_task_msg, my_task_hint1, my_task_hint2, my_task_hint3 = get_my_task(task_resource_path, parameters) #, my_task_blog
print(f"My task: {my_task_msg}\n \
      Hint1: {my_task_hint1}\n \
      Hint2: {my_task_hint2}\n \
      Hint3: {my_task_hint3}") 

# Send the answer
my_question = {
    "question": "What is the capital of Poland?"
    }
print(f"My question: {my_question}")
YESNO_verification = get_answer_2_question(my_question, mytask_token)

answer = {
    "answer": YESNO_verification
    }

answer_resource_path = str(resource + "/answer/" + mytask_token)
accomplish = send_my_answer(answer_resource_path, answer)