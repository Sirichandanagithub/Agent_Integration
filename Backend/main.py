# backend/main.py
from graph.workflow import app


while True:

    query = input("You: ")

    # Exit chatbot
    if query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    try:
        # Initial workflow state
        state = {
            "query": query,
            "next_agent": "",
            "result": "",
            "messages": [],
            "metadata": {}
        }

        # Invoke workflow
        result = app.invoke(state)

        # Print response
        print(f"Bot: {result['result']}")

    except Exception as e:
        print(f"Error: {str(e)}")
# TODO 1:
# import app
#
# from:
# graph.workflow

# TODO 2:
# create infinite loop
#
# while True:


# TODO 3:
# take user input
#
# query = input("You: ")


# TODO 4:
# exit condition
#
# if query.lower() in:

# ["exit", "quit"]
#
# print:
# "Goodbye!"
#
# break


# TODO 5:
# create initial state
#
# {
#   "query": query,
#   "next_agent": "",
#   "result": "",
#   "messages": [],
#   "metadata": {}
# }


# TODO 6:
# invoke workflow
#
# result = app.invoke(state)


# TODO 7:
# print chatbot answer
#
# result["result"]
#
# format:
#
# Bot: <answer>


# TODO 8:
# wrap invoke in try/except
#
# print errors cleanly