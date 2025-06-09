from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
import os
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key= os.getenv("GOOGLE_API_KEY"))

def get_embedding(text: str):
    return embedding_model.embed_query(text) 