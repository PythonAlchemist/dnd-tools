from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore

from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

from llama_index.core import StorageContext
import os
import logging
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

documents = SimpleDirectoryReader("data").load_data()
# define LLM
# NOTE: at the time of demo, text-davinci-002 did not have rate-limit errors

llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
Settings.llm = llm
Settings.chunk_size = 512


graph_store = SimpleGraphStore()
storage_context = StorageContext.from_defaults(graph_store=graph_store)

# NOTE: can take a while!
index = KnowledgeGraphIndex.from_documents(
    documents,
    max_triplets_per_chunk=2,
    storage_context=storage_context,
)
