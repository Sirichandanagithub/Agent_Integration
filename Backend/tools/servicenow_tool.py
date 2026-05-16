# backend/tools/servicenow_tool.py

import requests
from langchain.tools import tool
from config import get_settings


# Load settings from .env
settings = get_settings()


# Priority mapping
PRIORITY_MAP = {
    "1": "P1 - Critical",
    "2": "P2 - High",
    "3": "P3 - Medium",
    "4": "P4 - Low",
}


# State mapping
STATE_MAP = {
    "1": "Open",
    "2": "In Progress",
    "3": "On Hold",
    "6": "Resolved",
    "7": "Closed",
}


def _auth():
    """
    Returns ServiceNow username/password tuple.
    """
    return (
        settings.SNOW_USERNAME,
        settings.SNOW_PASSWORD
    )


def _headers():
    """
    Standard headers for ServiceNow API.
    """
    return {
        "Accept": "application/json"
    }


def _format_incidents(records: list) -> str:
    """
    Convert raw ServiceNow JSON into readable text.
    """

    if not records:
        return "No incidents found."

    lines = []

    for r in records:
        assigned_data = r.get("assigned_to")
        if isinstance(assigned_data, dict):
            assigned = assigned_data.get(
        "display_value",
        "Unassigned")
        elif isinstance(assigned_data, str):
            assigned = assigned_data
        else:
            assigned = "Unassigned"

        priority = PRIORITY_MAP.get(
            str(r.get("priority", "")),
            "Unknown"
        )

        state = STATE_MAP.get(
            str(r.get("state", "")),
            "Unknown"
        )

        line = (
            f"ID: {r.get('number', 'N/A')} | "
            f"Issue: {r.get('short_description', 'No description')} | "
            f"Priority: {priority} | "
            f"State: {state} | "
            f"Assigned to: {assigned}"
        )

        lines.append(line)

    return (
        f"Found {len(lines)} incident(s):\n"
        + "\n".join(lines)
    )


@tool
def query_incidents(filter_str: str) -> str:
    """
    Query ServiceNow incidents table.
    """

    try:
        response = requests.get(
            url=f"{settings.SNOW_INSTANCE_URL}/api/now/table/incident",

            auth=_auth(),

            headers=_headers(),

            params={
                "sysparm_query": filter_str,
                "sysparm_limit": 10,
                "sysparm_fields": (
                    "number,"
                    "short_description,"
                    "priority,"
                    "state,"
                    "assigned_to,"
                    "category"
                ),
            },

            timeout=10,
        )

        response.raise_for_status()

        result = response.json().get("result", [])

        return _format_incidents(result)

    except Exception as e:
        return f"Error querying incidents: {str(e)}"


@tool
def get_incident_by_id(incident_number: str) -> str:
    """
    Fetch a single incident by incident number.
    Example:
    INC001234
    """

    try:
        z = f"number={incident_number}"

        response = requests.get(
            url=f"{settings.SNOW_INSTANCE_URL}/api/now/table/incident",

            auth=_auth(),

            headers=_headers(),

            params={
                "sysparm_query": z,
                "sysparm_limit": 1,
                "sysparm_fields": (
                    "number,"
                    "short_description,"
                    "priority,"
                    "state,"
                    "assigned_to,"
                    "category"
                ),
            },

            timeout=10,
        )

        response.raise_for_status()

        result = response.json().get("result", [])

        return _format_incidents(result)

    except Exception as e:
        return f"Error querying incidents: {str(e)}"