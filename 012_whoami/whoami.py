import requests
import os
import json
import re
import time
from openai import OpenAI

print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\012_whoami\\"
os.chdir(path)
print(os.getcwd())

my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "/token/whoami"
resource_path = str(resource + taskname)

client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
MODEL = "gpt-4"

SYSTEM = """
Jesteś pasjonatem ciekawostek o znanych osobach. 
Z dużą łątwością odgadujesz, o kogo chodzi, na podstawie pojedynczych informacji.
Podam Ci kilka ciekawostek na temat znanej osoby, a Ty odpowiesz, o kogo chodzi.
Jeśli nie wiesz, o kogo chodzi, odpowiedz samym "Nie wiem".
Jeśli domyślasz się, o kogo chodzi, podaj imię i nazwisko tej osoby, i nic więcej.
"""

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
    return my_task.json()['msg'], my_task.json()['hint'] #, my_task.json()['input'], my_task.json()['question']

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


def whoami_answer(task_resource_path, parameters):
    do_you_know = "Nie wiem"
    ciekawostki_lista = []
    ciekawostki = ""
    while do_you_know == "Nie wiem":
        _, ciekawostka = get_my_task(task_resource_path, parameters)
        ciekawostki_lista.append(ciekawostka)
        for news in ciekawostki_lista:
            ciekawostki += "###\n" + news + "\n###\n"
        print(f"Ciekawostki: {ciekawostki}")
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"Czy wiesz o kogo chodzi? Oto ciekawostki:\n{ciekawostki}"}
                ],
            temperature = 0
            )
        do_you_know = str(response.choices[0].message.content)
        print(f"Wiem? {do_you_know}")
        time.sleep(3)
    whoami_answer = response.choices[0].message.content
    print(f"Celebryta: {whoami_answer}")
    
    
    return whoami_answer

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
my_task_msg, my_task_hint = get_my_task(task_resource_path, parameters) #, my_task_input, my_task_question, my_task_hint1, my_task_hint2, my_task_hint3
print(f"My task: {my_task_msg}\nHint: {my_task_hint}") #\nInput: {my_task_input}\nQuestion: {my_task_question}

# Send the answer

guessed_who = whoami_answer(task_resource_path, parameters)

answer = {
    "answer": guessed_who
    }

answer_resource_path = str(resource + "/answer/" + mytask_token)
accomplish = send_my_answer(answer_resource_path, answer)