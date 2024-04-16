"""
Rozwiąż zadanie API o nazwie 'tools'. Celem zadania jest zdecydowanie, 
czy podane przez API zadanie powinno zostać dodane do listy zadań (ToDo), 
czy do kalendarza (jeśli ma ustaloną datę). 
Oba narzędzia mają lekko różniące się od siebie definicje struktury JSON-a 
(różnią się jednym polem). Spraw, aby Twoja aplikacja działała poprawnie 
na każdym zestawie danych testowych.
"""

import requests
import os
import json
from openai import OpenAI
import uuid
import task_ops_framework



my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "tools"

openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
CHAT_MODEL = "gpt-4"


print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\016_tools\\"
os.chdir(path)
print(os.getcwd())


def find_intention(my_task_question):
    intention_system_content = """
        Jesteś specjalistą w rozpoznawaniu intencji użytkownika.
        Zastanów się, o co dokładnie prosi użytkownik.
        Jeśli w tekście od użytkownika znajduje się informacja o dacie, 
        najprawdopodobniej prośba dotyczy akcji związanej z aplikacją Calendar. 
        Wybierz tylko jedną z dwóch aplikach:
        - ToDo
        - Calendar
        Odpowiedź zwróć w formacie JSON, według wzoru.
        WZÓR:
        ###
        Wzór dla ToDo: Przypomnij mi, że mam kupić mleko = {"tool":"ToDo","desc":"Kup mleko" }
        Wzór dla Calendar: Jutro mam spotkanie z Marianem = {"tool":"Calendar","desc":"Spotkanie z Marianem","date":"2024-04-17"}
        ###
        """

    response = openai_client.chat.completions.create(
        messages=[
                {"role": "system", "content": intention_system_content},
                {"role": "user", "content": my_task_question}
                ],
        temperature = 0,
        model=CHAT_MODEL
    )
    return response.choices[0].message.content



task_ops_client = task_ops_framework.TaskMainOps()

# Get the token value of the task
my_task_token = task_ops_client.get_token(taskname)

# Get the content of the task and references
my_task_msg = task_ops_client.fetch_task(my_task_token) 

my_task_question = my_task_msg['question']
print(f"My task question: {my_task_question}")

# Submit answer
answer = find_intention(my_task_question)
answer_json = json.loads(answer)
print(f"Answer: {answer_json}\nAnswer type: {type(answer_json)}")
my_result = task_ops_client.submit_answer(answer_json, my_task_token)
