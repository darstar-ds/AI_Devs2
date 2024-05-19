"""
Rozwiąż zadanie API o nazwie 'ownapi'. 
Zadanie polega na zbudowaniu prostego API webowego, 
które będzie odpowiadać na pytania zadawane przez nasz system sprawdzania zadań. 
Adres URL do API działającego po HTTPS prześlij w polu 'answer' do endpointa /answer/. 
System na wskazany adres URL wyśle serię pytań (po jednym na żądanie). 
Swoje API możesz hostować na dowolnej platformie no-code (Make/N8N), 
jak i na własnym serwerze VPS, czy hostingu współdzielonym. 
Możesz też hostowac to API na własnym komputerze i wystawić nam je np. za pomocą usługi NGROK. 
Jeśli nadal komunikacja z API jest niejasna, przeczytaj hinta https://tasks.aidevs.pl/hint/ownapi
"""

"""
ownapi
curl -X POST -H "Content-Type: application/json" -d "{\"question\":\"Kto wynalazł rower?\"}" https://hook.eu2.make.com/fkyneubrxyx2u6pjhmgn14xro6c6v2kt    
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



my_OpenAI_key = os.environ.get("API_OPENAI_KEY")
my_AIDEVS2_key = os.environ.get("API_AIDEVS2_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "ownapipro"

openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
CHAT_MODEL = "gpt-4-turbo"


print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\018_ownapi\\"
os.chdir(path)
print(os.getcwd())

webhook_url = "https://hook.eu2.make.com/498vy7vep8d5gxxsxf8biriykwncmlrp"
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
