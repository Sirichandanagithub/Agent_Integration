# backend/graph/workflow.py

# TODO 1:
# import StateGraph, END
#
# from:
# langgraph.graph

from langgraph.graph import StateGraph, END
from graph.state import AgentState
from agents.router_agent import router_node
from agents.servicenow_agent import servicenow_node

def route_agent(state: AgentState):
    return state.get(
        "next_agent",
        "servicenow"
    )


workflow = StateGraph(AgentState)
workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "servicenow",
    servicenow_node
)
workflow.set_entry_point(
    "router"
)
workflow.add_conditional_edges(
    "router",

    route_agent,

    {
        "servicenow": "servicenow",
        "snowflake": END
    }
)

workflow.add_edge(
    "servicenow",
    END
)

app=workflow.compile()
# TODO 5:
# create function:
#
# route_agent(state: AgentState)
#
# PURPOSE:
# read state["next_agent"]
#
# return:
#
# state["next_agent"]
#
# fallback:
#
# "servicenow"


# TODO 6:
# create graph
#
# workflow = StateGraph(AgentState)


# TODO 7:
# add nodes
#
# router
# → router_node
#
# servicenow
# → servicenow_node


# TODO 8:
# set entry point
#
# router


# TODO 9:
# add conditional edges
#
# from:
# router
#
# function:
# route_agent
#
# mapping:
#
# {
#   "servicenow": "servicenow",
#   "snowflake": END
# }
#
# NOTE:
# we don't have snowflake yet
# so temporarily END


# TODO 10:
# add edge
#
# servicenow
# → END


# TODO 11:
# compile graph
#
# app = workflow.compile()