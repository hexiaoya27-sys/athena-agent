from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
import operator

class AthenaState(TypedDict):
    user_input: str
    user_id: str
    session_id: str
    messages: Annotated[List[BaseMessage], operator.add]
    reply: str
