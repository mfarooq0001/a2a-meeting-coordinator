# Agent card

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill
)
from agent import AvaAgent
from agent_executor import AvaAgentExecutor
from a2a.server.request_handler import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, InMemoryPushNotifier
import httpx
import uvicorn


def main(host="localhost", port=10003):

    # Define agent skill
    skill = AgentSkill(
        name="Meeting Scheduling",
        description="Helps schedule meetings and manage calendars for Ava Smith.",
        tags = ["scheduling", "calendar", "meetings"],
        examples = ["Schedule a meeting with John next week at 3 PM."]
    )
    # Define agent card
    agent_card = AgentCard(
        name="Ava Agent",
        description="An AI assistant designed to help schedule meetings for Ms. Ava Smith.",
        url = f"https://{host}/{port}"
        version = "1.0.0",
        defaultInputModes=AvaAgent.CONTENT_TYPES,
        defaultOutputModes=AvaAgent.CONTENT_TYPES,
        capabilities=AgentCapabilities(),
        skills=[
            AgentSkill.MEETING_SCHEDULING,
            AgentSkill.CALENDAR_MANAGEMENT,
        ],
    )

    # Request handler
    httpx_client = httpx.AsyncClient()
    request_handler = DefaultRequestHandler(
        agent_executor=AvaAgentExecutor(),
        task_store = InMemoryTaskStore(),
        push_notification_client=InMemoryPushNotifier(httpx_client=httpx_client),
    )

    # Host the app
    server = A2AStarletteApplication(
        agent_card=agent_card,
        request_handler=request_handler,
    )
    
    # Run the server
    uvicorn.run(server.build(), host=host, port=port)

if __name__ == "__main__":
    main()
