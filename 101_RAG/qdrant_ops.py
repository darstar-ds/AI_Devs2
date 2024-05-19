from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
import embedder
import os

qdrant_client = QdrantClient(url="http://localhost:6333")

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
                vectors_config=VectorParams(size=self.vector_length, distance=Distance.COSINE),
                )
            
    def add_vectors_2_collection(self):
            # Build a list of txt files with text chunks for embedding
            files_in_directory = os.listdir(self.chunks_path)
            txt_files = [file for file in files_in_directory if file.endswith('.txt')]
            
            #Add records to database
            print("Adding records to qdrant database...")
            
            for chunk in txt_files[:3]: #
                #Set UUID for a chunk
                chunk_id = str(uuid.uuid4())
                print(f"UUID: {chunk_id}")
                # chunk['UUID'] = chunk_id
                print(f"Item: {chunk}")

                #Set chunk content value
                with open(chunk, 'r') as file:
                    chunk_content = file.read()
                print(f"Cały chunk_content: {chunk_content}")

                #Set vector for a chunk
                getting_vector = embedder.embedder(self.chunks_path)
                if self.embedder_name == "hf_embedder":
                    chunk_vector = getting_vector.get_embedding_from_hf(chunk_content)
                elif self.embedder_name == "mistral_embedder":
                    chunk_vector = getting_vector.get_embedding_from_mistral(chunk_content)
                elif self.embedder_name == "st_embedder":
                    chunk_vector = getting_vector.get_embedding_from_st(chunk_content) 
                print(f"Vector: {chunk_vector[:3]}")
                                
                #Upload item to qdrant database
                qdrant_client.upsert(
                    collection_name=self.my_collection_name,
                    points=[
                        PointStruct(
                            id=chunk_id,
                            vector=chunk_vector,
                            payload=chunk_content
                            )
                        ]
                    )
            # Dump new_people_data to JSON file
            # with open('new_people_data.json', 'w') as outfile:
            #     json.dump(new_people_data, outfile)
            #     print("new_people_data.json dumped to disk.")