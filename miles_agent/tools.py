from typing import Dict
from datetime import datetime

# In-memory database for meeting place schedules:
# mapping date -> time slots -> meeting name / status
MEETING_SCHEDULE: Dict[str, Dict[str, str]] = {}

# --- Dummy global data ---
MEETING_SCHEDULE = {
    "2025-11-13": {
        "09:00": "unknown",
        "10:00": "unknown",
        "11:00": "unknown",
    },
    "2025-11-14": {
        "08:30": "unknown",
        "09:30": "busy",
        "10:30": "unknown",
        "11:30": "available",
    },
    "2025-11-15": {
        "09:00": "unknown",
        "10:00": "busy",
        "11:00": "unknown",
    },
}

def generate_meeting_schedule():
    """Dummy: Pretend to generate a fixed 3-day meeting schedule."""
    print("Dummy meeting schedule initialized with fixed test dates and times.")

# Initialize dummy schedule
generate_meeting_schedule()


def list_meeting_availabilities(date: str) -> dict:
    """
    List available and booked time slots for a given date.
    """
    if date not in MEETING_SCHEDULE:
        return {
            "status": "error",
            "message": f"No meeting schedule found for {date}. Try another date.",
            "schedule": {},
        }

    daily_schedule = MEETING_SCHEDULE[date]
    available_slots = [t for t, v in daily_schedule.items() if v == "unknown"]
    booked_slots = {t: v for t, v in daily_schedule.items() if v != "unknown"}

    return {
        "status": "success",
        "message": f"Meeting schedule for {date}.",
        "available_slots": available_slots,
        "booked_slots": booked_slots,
    }


def book_meeting_place(
    date: str,
    start_time: str,
    end_time: str,
    meeting_name: str
) -> dict:
    """
    Dummy version: allows booking only for available single-hour slots.
    """
    if date not in MEETING_SCHEDULE:
        return {"status": "error", "message": f"No meeting schedule for {date}."}

    # For simplicity, ignore end_time; only single-hour slots allowed
    if start_time not in MEETING_SCHEDULE[date]:
        return {
            "status": "error",
            "message": "Invalid time slot. Try 08:00, 09:00, or 10:00."
        }

    if MEETING_SCHEDULE[date][start_time] != "unknown":
        return {
            "status": "error",
            "message": (
                f"Slot {start_time} on {date} is already booked for "
                f"{MEETING_SCHEDULE[date][start_time]}."
            ),
        }

    MEETING_SCHEDULE[date][start_time] = meeting_name

    return {
        "status": "success",
        "message": f"Meeting '{meeting_name}' scheduled on {date} at {start_time}.",
    }
