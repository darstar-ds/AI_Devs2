"""
Rozwiąż zadanie API o nazwie 'md2html'. 
Twoim celem jest stworzenie za pomocą fine-tuningu modelu, 
który po otrzymaniu pliku Markdown na wejściu, 
zwróci jego sformatowaną w HTML wersję. Mamy tutaj jedno drobne utrudnienie, 
ponieważ znacznik pogrubienia jest konwertowany w bardzo nietypowy sposób.

Oto jak wygląda konwersja do HTML, którą chcemy otrzymać:

# Nagłówek1 = <h1>Nagłówek1</h1>
## Nagłówek2 = <h2>Nagłówek2</h2>
### Nagłówek3= <h3>Nagłówek3</h3>
**pogrubienie** = <span class="bold">pogrubienie</span>
*kursywa* = <em>kursywa</em>
[AI Devs 3.0](https://aidevs.pl) = <a href="https://aidevs.pl">AI Devs 3.0</a>
_podkreślenie_ = <u>podkreślenie</u>

Zaawansowana konwersja:
1. Element listy
2. Kolejny elementy

Wynik:
<ol>
<li>Element listy</li>
<li>Kolejny element</li>
</ol>

Tekst otrzymany z endpointa /task/ musisz przepuścić przez swój, wytrenowany model, 
a następnie zwrócić w standardowy sposób do /answer/.

Uwaga: do fine-tuningu użyj modelu gpt-3.5-turbo-0125. 
Istnieje ogromna szansa, że przy pierwszych podejściach do nauki modelu 
otrzymasz bardzo częste halucynacje. 
Zwiększ liczbę przykładów w pliku użytym do nauki i/lub 
pomyśl o zwiększeniu liczby cykli szkoleniowych. 
To zadanie da się rozwiązać bez fine tuningu, ale zależy nam, 
abyś jako kursant zaznajomił się z procesem uczenia modeli nowych umiejętności.

Dane wejściowe mogą zawierać zagnieżdżone znaczniki:

# Bardzo _ważny_ tekst = <h1> Bardzo <u>ważny</u> tekst</h1>
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
resource = "https://tasks.aidevs.pl"
taskname = "md2html"


openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
CHAT_MODEL = "ft:gpt-3.5-turbo-1106:starosta:ds:9GYFFILK"


print(os.getcwd())
path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\022_md2html\\"
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


def md2html(md2convert):
    system_content = """
                    Convert the MD format provided by the user into HMTL format.
                    Focus on bold converting rule.
                    Important is to keep the format of links according the rule below.
                    Let's also concentrate on underlined fragments as follow.

                    RULES:
                    **pogrubienie** = <span class="bold">pogrubienie</span>
                    [AI Devs 3.0](https://aidevs.pl) = <a href="https://aidevs.pl">AI Devs 3.0</a> 
                    _podkreślenie_ = <u>podkreślenie</u>
                    """
    response = openai_client.chat.completions.create(
        messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": md2convert}
                ],
        temperature = 0,
        model=CHAT_MODEL,
        # max_tokens=20,
    )
    return response.choices[0].message.content 
    




task_ops_client = task_ops_framework.TaskMainOps()

# Get the token value of the task
my_task_token = task_ops_client.get_token(taskname)

# Get the content of the task and references
my_task_msg = task_ops_client.fetch_task(my_task_token) 

md2convert = my_task_msg['input']
my_task_html = md2html(md2convert)
print(f"MD2convert:\n{md2convert}\nHTML:\n{my_task_html}")


# Submit answer
answer = my_task_html
# print(f"Answer: {answer}\nAnswer type: {type(answer)}")
my_result = task_ops_client.submit_answer(answer, my_task_token)
