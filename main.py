from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
import getpass
import os
import qdrant_client
from qdrant_client.http import models
from qdrant_client import QdrantClient
from langchain.memory import ConversationBufferMemory  # Import the memory

# Initialize the QdrantClient with the Qdrant server URL and API key

qdrant_client = QdrantClient(
    url="<<--ENTER THE QDRANT URL HERE-->", 
    api_key="<--ENTER YOUR QDRANT API KEY HERE-->",
)


[[[ #IF YOU NEED TO CREATE A COLLECTION (
qdrant_client.create_collection(
    collection_name="NAME A COLLECTION OF YOUR CHOICE",
    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
)]]]]


os.environ["OpenAI_API_Key"] ="<<--ENTER YOUR OPEN AI API KEY HERE-->>"
embeddings = OpenAIEmbeddings()
vector_store = Qdrant(
    client=qdrant_client, collection_name="<--ENTER THE NAME OF THE COLLECTION YOU CREATED EARLIER-->", 
    embeddings=embeddings,
)


def get_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = "/n",
        chunk_size=1000, 
        chunk_overlap= 200,
        length_function=len
        )
    chunks = text_splitter.split_text(text)
    return chunks


with open('story.txt') as f:
    raw_text = f.read()

texts=get_chunks(raw_text) 
vector_store.add_texts(texts)



memory = ConversationBufferMemory()


# Create the RetrievalQA chain with memory

from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
qa = RetrievalQA.from_chain_type( llm=OpenAI(), chain_type = "stuff",
                                 retriever= vector_store.as_retriever(),
                                 memory=memory
                                )



# querry = "Who is Luna?"
# response = qa.invoke(querry)  # Now the conversation history will be stored
# print(response)

