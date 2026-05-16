# backend/graph/state.py

# TODO 1: Import TypedDict from typing
# TODO 2: Import List, Any from typing

from typing import TypedDict
from typing import List,Any 

class AgentState(TypedDict):
    query:str
    next_agent: str
    result: str
    messages: List[Any]
    metadata: dict


# TODO 3: Create AgentState class extending TypedDict with these fields:
#   - query: str
#         the original user message, never modified after set
#
#   - next_agent: str
#         set by router_node to tell workflow which agent runs next
#         values will be: 'servicenow' or 'snowflake'
#
#   - result: str
#         the final answer written by the specialist agent
#         this is what gets sent back to the frontend
#
#   - messages: List[Any]
#         conversation history loaded from memory.py
#         passed so agents know what was said before
#
#   - metadata: dict
#         flexible bag for extra info like:
#         which agent was used, filters applied, any errors