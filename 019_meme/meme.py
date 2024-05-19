"""
Wykonaj zadanie API o nazwie “meme”. 
Celem zadania jest nauczenie Cię pracy z generatorami grafik i dokumentów. 
Zadanie polega na wygenerowaniu mema z podanego obrazka i podanego tekstu. 
Mem ma być obrazkiem JPG o wymiarach 1080x1080. 
Powinien posiadać czarne tło, dostarczoną grafikę na środku i podpis zawierający dostarczony tekst. 
Grafikę z memem możesz wygenerować za pomocą darmowych tokenów dostępnych w usłudze RenderForm 
(50 pierwszych grafik jest darmowych). 
URL do wygenerowanej grafiki spełniającej wymagania wyślij do endpointa /answer/. 
W razie jakichkolwiek problemów możesz sprawdzić hinty https://tasks.aidevs.pl/hint/meme 
Ideą jest pokazanie Ci prostej metody na generowanie obrazów i dokumentów (np. PDF)
 z użyciem technologii no-code. 
 Może to być np. użyteczne przy generowaniu faktur, certyfikatów itp. 
 Ta wiedza z pewnością Ci się przy automatyzacji procesów biznesowych."""

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
my_RENDERFORM_key = os.environ.get("API_RENDERFORM_KEY")
resource = "https://tasks.aidevs.pl"
taskname = "meme"
rf_template_id = "strange-tigers-sting-tightly-1314"

openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
CHAT_MODEL = "gpt-4-turbo"


print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\019_meme\\"
os.chdir(path)
print(os.getcwd())

webhook_url = "https://hook.eu2.make.com/498vy7vep8d5gxxsxf8biriykwncmlrp"
params = {
    "question": "Kto wynalazł rower?"
}

def get_image(url, img_name):
    image = requests.get(url)
    if image.status_code == 200:
        # Open the file for writing in binary mode
        with open(img_name, 'wb') as file:
            file.write(image.content)
        print(f"The PNG file has been saved as {img_name}.")
    else:
        print(f"Failed to retrieve the image. Status code: {image.status_code}")
    return image


def render_image(temp_id, my_img, my_text):
    api_url = "https://get.renderform.io/api/v2/render"
    headers = {
        'X-API-KEY': my_RENDERFORM_key,
        'Content-Type': 'application/json'
    }
    payload = {
        "template": temp_id,
        "data": {
            "DS_meme_text.text": my_text,
            "DS_meme_image.src": my_img
            }
        }
    
    try:
        render_meme = requests.post(api_url, data=json.dumps(payload), headers=headers)
        render_meme.raise_for_status()
        print(render_meme.json()['href'])
        if render_meme.status_code == 200:
            get_image(render_meme.json()['href'], "my_downloaded_meme.png")
        else:
            print(f"Failed to retrieve the image. Status code: {render_meme.status_code}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')
        print(f'Response content: {render_meme.content}')  # This will show more details
        raise    
    return render_meme.json()['href']
    




task_ops_client = task_ops_framework.TaskMainOps()

# Get the token value of the task
my_task_token = task_ops_client.get_token(taskname)

# Get the content of the task and references
my_task_msg = task_ops_client.fetch_task(my_task_token) 

my_task_image_url = my_task_msg['image']
my_task_image = get_image(my_task_image_url, "downloaded_image.png")
my_task_text = my_task_msg['text']
print(f"Tekst do mema: {my_task_text}")

my_meme = render_image(rf_template_id, my_task_image_url, my_task_text)

# Submit answer
answer = my_meme
# print(f"Answer: {answer}\nAnswer type: {type(answer)}")
my_result = task_ops_client.submit_answer(answer, my_task_token)
