from promptflow import tool
from promptflow.connections import CognitiveSearchConnection

from azure.core.credentials import AzureKeyCredential 
from typing import List
import inspect
from pip._vendor import pkg_resources

from azure.search.documents.models import Vector
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(query_text: str, filename: str, embedding: List[float], index_name: str, search_conn: CognitiveSearchConnection) -> str:
  
  def nonewlines(s: str) -> str:
    return s.replace('\n', ' ').replace('\r', ' ')

  def get_version(package):
    package = package.lower()
    return next((p.version for p in pkg_resources.working_set if p.project_name.lower() == package), "No match")
  

  print(get_version("azure-search-documents"))
  search_client = SearchClient(
    endpoint=search_conn.api_base,
    credential=AzureKeyCredential(search_conn.api_key),
    index_name=index_name
  )
  # Question: What is Woodside's operating revenue in 2022?
  if filename is not None:
      filter=f"sourcefile eq '{filename}'"
  else:
      filter = None
  top=3
  print(f"Filter is {filter}")
  vector = Vector(value=embedding, k=3, fields="embedding")
  #imageVector = Vector(value=florence_embedding, k=3, fields="imageEmbedding")

  #results = search_client.search(  
  #  search_text=None,  
  #  vectors= [vector],
  #  select=["sourcepage", "embedding", "content"],
  #  query_language="en-us"
#)  
  query = query_text
  #print(inspect.signature(SearchClient.search))
  r = search_client.search(query, 
                                filter=filter, 
                                query_type="semantic",
                                query_language="en-us", 
                                query_speller="lexicon", 
                                semantic_configuration_name="default", 
                                top=top, 
                                query_caption=None,
                                vectors=[vector], 
                                #top_k=50, 
                                #vector_fields="embedding"
  )
  results = [doc["sourcepage"] + ": " + nonewlines(doc["content"]) for doc in r]
  content = "\n".join(results)
  #content = "bob"
  return content