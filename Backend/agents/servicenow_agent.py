from langchain_core.prompts import ChatPromptTemplate
from graph.state import AgentState
from config import get_llm
from tools.servicenow_tool import (
    query_incidents,
    get_incident_by_id
)


SERVICENOW_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a ServiceNow support agent.

You help users answer incident questions.

Available tools:

query_incidents(filter)
→ fetch incidents

get_incident_by_id(number)
→ fetch specific incident

Rules:
- Use tools whenever needed
- Be concise
- If incident ID present:
  use get_incident_by_id

Examples:

show open incidents
→ query_incidents("state=1")

find INC001234
→ get_incident_by_id("INC001234")
"""
    ),

    ("human", "{query}")
])


def servicenow_node(state: AgentState) -> dict:
    """
    ServiceNow specialist agent.
    """

    llm = get_llm()

    llm_with_tools = llm.bind_tools([
        query_incidents,
        get_incident_by_id
    ])

    chain = SERVICENOW_PROMPT | llm_with_tools

    response = chain.invoke({
        "query": state["query"]
    })

    # Gemini requested a tool
    if hasattr(response, "tool_calls") and response.tool_calls:

        tool_call = response.tool_calls[0]

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        try:
            if tool_name == "query_incidents":
                result = query_incidents.invoke(tool_args)

            elif tool_name == "get_incident_by_id":
                result = get_incident_by_id.invoke(tool_args)

            else:
                result = "Unknown tool requested."

            return {
                "result": result
            }

        except Exception as e:
            return {
                "result": f"Tool error: {str(e)}"
            }

    # Normal text response
    return {
        "result": str(response.content)
    }