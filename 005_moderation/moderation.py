import requests
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/moderation"
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
    return my_task.json()['msg'], my_task.json()['input']

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

def moderate_sentences(sentences):
    flagged_table = []
    for sentence in sentences:
        response = client.moderations.create(input=sentence)
        response_json = json.loads(response.model_dump_json())
        print(response_json)
        flagged = response_json['results'][0]['flagged']
        
        # add 1 if True to flagged_table list
        if flagged == True:
            flagged_table.append(1)
        else:
            flagged_table.append(0) 

        categories = response_json['results'][0]['categories']
        category_scores = response_json['results'][0]['category_scores']
        print("Flagged:", flagged)
        print("Categories:", categories)
        print("Category Scores:", category_scores)
    return flagged_table

parameters = {
    "apikey": my_AIDEVS2_key
    }

print(f"My API key: {my_AIDEVS2_key}")
print(f"Resource path: {resource_path}")
print(parameters)

# Get the token value of the task
mytask_token = get_my_token(resource_path, parameters)
print(f"Token value: {mytask_token}")

# Get the content of the task and references
task_resource_path = str(resource + "/task/" + mytask_token)
my_task_msg, my_task_sentences = get_my_task(task_resource_path, parameters)
print(f"My task: {my_task_msg}\nSentences 4 moderation: {my_task_sentences}")

# Send the answer
flagged_table = moderate_sentences(my_task_sentences)
print(flagged_table)
answer = {
    "answer": flagged_table
    }

answer_resource_path = str(resource + "/answer/" + mytask_token)
accomplish = send_my_answer(answer_resource_path, answer)