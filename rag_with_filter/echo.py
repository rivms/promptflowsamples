from promptflow import tool
import json


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> object:
    j = json.loads(input1)
    return j
    #return {"query": j.query, "file_name": j.file_name}