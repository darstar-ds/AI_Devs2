import json
import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))

MODEL="gpt-4" #"gpt-3.5-turbo"

conversation=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"},
    {"role": "assistant", "content": "The 2020 World Series was played at Globe Life Field in Arlington, Texas."},
    {"role": "user", "content": "Which team won Football World Championships in 2020?"}
  ]



response = client.chat.completions.create(
  model=MODEL,
  messages=conversation,
  temperature=0,
)

print(json.dumps(json.loads(response.model_dump_json()), indent=4))

# print(response.choices[0].message.content)
