
# %%
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from sentence_transformers import SentenceTransformer, util
from PIL import Image
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import os
from llama_index.llms.together import TogetherLLM
from llama_index.core.llms import ChatMessage
from langchain.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.prompts import ChatPromptTemplate
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("API_KEY")

def embed(): 
    Settings.embed_model = "clip"
    #Load CLIP model
    model = SentenceTransformer('clip-ViT-B-32')

    import qdrant_client
    from llama_index.core import SimpleDirectoryReader


    # Create a local Qdrant vector store
    client = qdrant_client.QdrantClient(path="qdrant_img_db_2")

    text_store = QdrantVectorStore(
        client=client, collection_name="text_collection"
    )
    image_store = QdrantVectorStore(
        client=client, collection_name="image_collection"
    )
    storage_context = StorageContext.from_defaults(
        vector_store=text_store, image_store=image_store
    )
    lc_embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
    )
    embed_model = LangchainEmbedding(lc_embed_model)

    documents = SimpleDirectoryReader("./SOURCE_DOCUMENTS").load_data()
    index2 = VectorStoreIndex.from_documents(documents, embed_model=embed_model,storage_context=storage_context)
    return index2

index2 = embed()
def query(input):
    while True:
            query = input
            retriever2 = index2.as_retriever(similarity_top_k=3)
            retrieval_results = retriever2.retrieve(query)
            llm = TogetherLLM(
                    model="togethercomputer/llama-2-70b-chat", api_key=api_key
                )
            # %%
            os.environ['TOKENIZERS_PARALLELISM'] = 'false'
            Settings.llm = llm
            response = index2.as_query_engine().query(query)
            if not isinstance(response, str):
                # If the response is not a string, convert it to a string
                response = str(response)
            
            # Print the user query and the generated response
            print("user query:", query)
            print("answer:", response)
            
            # Return the response as a string
            return response


