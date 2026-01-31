# Tools for Ava's scheduling agent
from crewai.tools import BaseTool

# Dummy data representing Ava's availability
JOHN_AVAILABILITY = {
    "2026-02-03": "Available from 1:00 PM to 4:00 PM",
    "2026-02-04": "Busy until 3:30 PM, then available from 3:30 PM to 6:00 PM",
    "2026-02-05": "Available from 10:00 AM to 2:00 PM",
    "2026-02-06": "Available from 9:00 AM to 12:00 PM",
    "2026-02-07": "Unavailable (out of office)",
}

def check_john_availability(date_str: str) -> dict[str, str]:
    """Check John's availability for a given date.

    Args:
        date_str (str): The date to check in 'YYYY-MM-DD' format.
    
    Returns:
        dict[str, str]: A dictionary with the date and John's availability.
    """

    if not date_str:
        return {"status": "error": "No date provided."}

    availability = AVA_AVAILABILITY.get(date_str)

    if availability:
        return {
            "status": "success",
            "message": f"John's availability on {date_str}: {availability}"
        }
    
    return {
        "status": "input_required",
        "message": f"No availability information found for {date_str}. Please provide a different date."
    }


class AvailabilityTool(BaseTool):
    name: str = "Calendar Availability Checker"
    description: str = "Checks John's availability for a given date."

    def _run(self, date: str) -> str:
        return get_availability(date)["message"]