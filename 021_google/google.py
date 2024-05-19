"""
Rozwiąż zadanie API o nazwie 'google'. 
Do jego wykonania będziesz potrzebować darmowego konta w usłudze SerpAPI. 
Celem zadania jest samodzielne zaimplementowanie rozwiązania podobnego do tego, 
znanego z ChatGPT Plus, gdzie po wpisaniu zapytania na temat, 
o którym model nie ma pojęcia, uruchamiana jest wyszukiwarka BING. 
My posłużymy się wyszukiwarką Google, a Twój skrypt będzie wyszukiwał 
odpowiedzi na pytania automatu sprawdzającego i będzie zwracał je w czytelnej dla człowieka formie. 
Więcej informacji znajdziesz w treści zadania /task/, 
a podpowiedzi dostępne są pod https://tasks.aidevs.pl/hint/google.
"""

"""
c:\\Users\\dariu\\OneDrive\\Dokumenty\\Docker\\aidev2venv\\Scripts\\activate.bat
"""

import requests
import os
import json
from openai import OpenAI
import uuid
import task_ops_framework



my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
my_SERPAPI_key = os.environ.get("API_SERPAPI_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "google"


openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
CHAT_MODEL = "gpt-3.5-turbo"


print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\021_google\\"
os.chdir(path)
print(os.getcwd())


"""
ownapi
curl -X POST -H "Content-Type: application/json" -d "{\"question\":\"Jak jest adres polskiej witryny onet?\"}" https://hook.eu2.make.com/5ybhsv9roaw9juw3tpcm5pcr9rn6y3fl    
"""

"""
ownapipro
curl -X POST -H "Content-Type: application/json" -d "{\"question\":\"Kto wynalazł rower?\"}" https://hook.eu2.make.com/498vy7vep8d5gxxsxf8biriykwncmlrp    
"""
import requests
import os
import json
from openai import OpenAI
import uuid
import task_ops_framework

webhook_url = "https://hook.eu2.make.com/5ybhsv9roaw9juw3tpcm5pcr9rn6y3fl"
params = {
    "question": "Kto wynalazł rower?"
}

def send_q():
    headers = {'Content-Type': 'application/json'}
    try:
        webhook_answer = requests.post(webhook_url, json=params, headers=headers)
        webhook_answer.raise_for_status()
        print(webhook_answer.json())
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {webhook_answer.content}')  # This will show more details
        raise 
    




task_ops_client = task_ops_framework.TaskMainOps()

# Get the token value of the task
my_task_token = task_ops_client.get_token(taskname)

# Get the content of the task and references
my_task_msg = task_ops_client.fetch_task(my_task_token) 

# my_task_check_webhook = send_q()


# Submit answer
answer = webhook_url
# print(f"Answer: {answer}\nAnswer type: {type(answer)}")
my_result = task_ops_client.submit_answer(answer, my_task_token)
