from qdrant_client import QdrantClient, models
# from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
import embedder
import os
import datetime
import json

qdrant_client = QdrantClient(url="http://localhost:6333")
context_logs_path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\AI_Devs2\\101_RAG\\context_logs\\"

class ds_qdrant:
    def __init__(self, chunks_path, embedder_name, my_collection_name, vector_length):
            self.chunks_path = chunks_path
            self.embedder_name = embedder_name
            self.vector_length = vector_length
            self.my_collection_name = my_collection_name +"_" + str(self.vector_length)

    def create_collection_in_qdrant(self):
        if qdrant_client.collection_exists(collection_name=self.my_collection_name):
            print(f"The collection {self.my_collection_name} already exists.")
            pass
        else:
            print(f"The collection {self.my_collection_name} does not exist. Let's create one.")
            qdrant_client.create_collection(
                collection_name=self.my_collection_name,
                vectors_config=models.VectorParams(size=self.vector_length, distance=models.Distance.COSINE),
                )
            
    def add_vectors_2_collection(self):
            # Build a list of txt files with text chunks for embedding
            files_in_directory = os.listdir(self.chunks_path)
            txt_files = [file for file in files_in_directory if file.endswith('.txt')]
            # print(f"List of TXT files: {txt_files}")
            
            result = qdrant_client.get_collection(collection_name=self.my_collection_name)
            vectors_count = result.vectors_count
            print(f"Number of vectors in the collection: {vectors_count}")

            if vectors_count < 1:
                #Add records to database
                print("Adding records to qdrant database...")
                
                counter = 1
                for chunk in txt_files: #[:3]
                    #Set UUID for a chunk
                    chunk_id = str(uuid.uuid4())
                    if counter % 20 == 0:
                        print(f"UUID: {chunk_id}\nItem: {chunk}")

                    #Set chunk content value
                    with open(self.chunks_path+chunk, 'r', encoding='utf-8') as file:
                        chunk_content = file.read()
                    # print(f"100 chars of chunk_content: {chunk_content[:100]}")
                    payload_dict = {"content": chunk_content, "counter": counter}

                    #Set vector for a chunk
                    getting_vector = embedder.embedder(self.chunks_path)
                    if self.embedder_name == "hf_embedder":
                        chunk_vector = getting_vector.get_embedding_from_hf(chunk_content)
                    elif self.embedder_name == "mistral_embedder":
                        chunk_vector = getting_vector.get_embedding_from_mistral(chunk_content)
                    elif self.embedder_name == "st_embedder":
                        chunk_vector = getting_vector.get_embedding_from_st(chunk_content)
                    elif self.embedder_name == "openai_embedder":
                        chunk_vector = getting_vector.get_embedding_from_openai(chunk_content) 
                    # print(f"Vector: {chunk_vector[:3]}")
                                    
                    #Upload item to qdrant database
                    qdrant_client.upsert(
                        collection_name=self.my_collection_name,
                        points=[
                            models.PointStruct(
                                id=chunk_id,
                                vector=chunk_vector,
                                payload=payload_dict
                                )
                            ]
                        )
                    counter += 1
            else:
                print("There are already vectors in the collection. I add nothing.")
    
    
    def get_vector_4_txt(self, question):
        getting_vector = embedder.embedder(self.chunks_path)
        if self.embedder_name == "hf_embedder":
            chunk_vector = getting_vector.get_embedding_from_hf(question)
        elif self.embedder_name == "mistral_embedder":
            chunk_vector = getting_vector.get_embedding_from_mistral(question)
            chunk_vector = chunk_vector.values.tolist()[0]
        elif self.embedder_name == "st_embedder":
            chunk_vector = getting_vector.get_embedding_from_st(question) 
        elif self.embedder_name == "openai_embedder":
            chunk_vector = getting_vector.get_embedding_from_openai(question) 
        
        print(f"Question vector as list (first 3 values): {chunk_vector[:3]}")
        return chunk_vector


    def find_context(self, q_vector):
        query_results = qdrant_client.search(
            collection_name = self.my_collection_name,
            query_vector = q_vector,
            limit = 10
            )
        # print(f"query_results type: {type(query_results)}\nquery_results: {query_results}")
        return query_results


    def save_context_2_txt(self, query_results):          
        formatted_data = {}
        for i in range(0, len(query_results)):
            chunk_counter = query_results[i].payload['counter']
            chunk_content = query_results[i].payload['content']
            formatted_data[chunk_counter] = chunk_content
        # print(f"formatted_data type: {type(formatted_data)}\nformatted_data: {formatted_data}")
        curr_time = datetime.datetime.now()
        format_curr_time = curr_time.strftime("%Y-%m-%d_%H%M%S")

        with open(context_logs_path + format_curr_time + ".txt", 'w', encoding='utf-8') as file:
            file.write(json.dumps(formatted_data, indent=4))

        formatted_data_json = [{"counter": key, "content": value} for key, value in formatted_data.items()]
        return formatted_data_json


    def extend_context(self, counter_values):
        # print(f"counter_values: {counter_values}")
        five_ext_content = {}
        for mid_counter in counter_values:
            ext_counters = [int(mid_counter)-2, int(mid_counter)-1, int(mid_counter), int(mid_counter)+1, int(mid_counter)+2]  
            # print(f"ext_counter_values: {ext_counters}")
            
            for ext_counter in ext_counters:
                ext_content = qdrant_client.scroll(
                    collection_name=self.my_collection_name,
                    scroll_filter=models.Filter(
                        must=[
                            models.FieldCondition(key="counter", match=models.MatchValue(value=ext_counter)),
                        ]
                    ),
                    with_payload=True
                )
                five_ext_content_key = 'ext_counter_' + str(ext_counter)
                five_ext_content[five_ext_content_key] = ext_content[0][0].payload['content']

        # print(f"Extended content: {five_ext_content}\nExt_content_length: {len(five_ext_content)}")

        curr_time = datetime.datetime.now()
        format_curr_time = curr_time.strftime("%Y-%m-%d_%H%M%S")

        with open(context_logs_path + format_curr_time + "_ext" + ".txt", 'w', encoding='utf-8') as file:
            file.write(json.dumps(five_ext_content, indent=4))