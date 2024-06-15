import os
import requests
from openai import OpenAI
import pandas as pd
from mistralai.client import MistralClient
from sentence_transformers import SentenceTransformer


class embedder:
    def __init__(self, txt_path):
        self.txt_path = txt_path


    def get_embedding_from_hf(self, chunks):
        model_id = "sentence-transformers/all-MiniLM-L6-v2"
        hf_token = os.environ.get("API_HF_READ_TOKEN")
        api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
        headers = {"Authorization": f"Bearer {hf_token}"}

        response = requests.post(api_url, headers=headers, json={"inputs": chunks, "options":{"wait_for_model":True}})
        embedd = pd.DataFrame(response.json())
        print(embedd)
        print(embedd.shape)
        return embedd
    
    
    def get_embedding_from_st(self, chunks):
        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        embeddings = model.encode(chunks)
        embedd = pd.DataFrame(embeddings)
        embedd = embedd.T
        print(embedd)
        print(embedd.shape)
        return embedd
        

    def get_embedding_from_mistral(self, chunks):
        mistral_api_key = os.environ.get("API_MISTRAL_KEY")
        client = MistralClient(api_key=mistral_api_key)
        embeddings_batch_response = client.embeddings(
            model="mistral-embed",
            input=chunks
            )
        embedd = pd.DataFrame(embeddings_batch_response.data[0].embedding)
        embedd = embedd.T
        print(embedd)
        print(embedd.shape)
        return embedd
 
    def get_embedding_from_openai(self, chunks):
        openai_client = OpenAI(api_key=os.environ.get("API_OPENAI_KEY"))
        response = openai_client.embeddings.create(
            input=[chunks],
            model="text-embedding-3-large"
        )
        return response.data[0].embedding