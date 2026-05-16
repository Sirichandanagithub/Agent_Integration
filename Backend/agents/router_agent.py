# backend/agents/router_agent.py

from langchain_core.prompts import ChatPromptTemplate
from graph.state import AgentState
from config import get_llm


# Prompt that teaches Gemini how to route queries
ROUTER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a routing agent.

Your ONLY job is to choose ONE agent.

Available agents:

servicenow
→ incidents
→ tickets
→ IT issues
→ outages
→ priorities
→ assignment groups

snowflake
→ reports
→ analytics
→ dashboards
→ metrics

Rules:
- Reply ONLY with:
  servicenow
  OR
  snowflake

- No explanation
- No punctuation
- If unsure → servicenow

Examples:

show open incidents
→ servicenow

find INC001234
→ servicenow

show sales report
→ snowflake
"""
    ),

    ("human", "{query}")
])


def router_node(state: AgentState) -> dict:
    """
    Decide which agent should handle the user query.

    Reads:
        state["query"]

    Writes:
        state["next_agent"]

    Returns:
        dict that LangGraph merges into state
    """

    # Step 1: get Gemini LLM
    llm = get_llm()

    # Step 2: create chain
    chain = ROUTER_PROMPT | llm

    # Step 3: invoke Gemini
    response = chain.invoke({
        "query": state["query"]
    })

    # Step 4: clean response
    raw = response.content.strip().lower()

    # Step 5: extract first word
    agent_name = (
        raw.split()[0]
        if raw.split()
        else "servicenow"
    )

    # Step 6: validate output
    valid_agents = {
        "servicenow",
        "snowflake"
    }

    if agent_name not in valid_agents:
        agent_name = "servicenow"

    # Step 7: return state update
    return {
        "next_agent": agent_name,

        "metadata": {
            **state.get("metadata", {}),
            "agent_used": agent_name
        }
    }