# Miles  Agent Implementation (CrewAI)

from google.adk import Agent
from google.adk.tools.tool_context import ToolContext
from dotenv import load_dotenv
import asyncio
import datetime
import uuid
import httpx
import os

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse,
)

load_dotenv()

class MilesAgent:

    def __init__(self, remote_agent_urls):
        self.remote_agent_urls = remote_agent_urls or []
        self.remote_connections = {}
        self.cards = {}
        self.agent = None

    async def create_agent(self):
        
        await self._load_remote_agents()

        self.agent = Agent(
            model="gemini-2.0-flash",
            name="miles_agent",
            description="Helps coordinate meetings with friends",
            instruction=self._get_instruction(),
            tools=[self.send_message,
                   book_badminton_court, 
                   list_court_availabilities
                   ]
        )

        return self.agent

    def _get_instruction(self):
    """Describes what our Host Agent should do."""
    friends = "\n".join([card.name for card in self.cards.values()]) or "No friends yet"

    return f"""
        You are the Host Agent — a helpful coordinator.
        Your mission: schedule a meeting with your friends.

        - Ask friends for availability starting from tomorrow.
        - Find a common available time.
        - Confirm the meeting details with everyone.
        - Schedule the meeting once confirmed.

        **Friends:**
        {friends}

        **Today's date**
        {datetime.datetime.now()}
        """
    
    async def _load_remote_agents(self):
        async with httpx.AsyncClient(timeout=30) as client:
            for url in self.remote_agent_urls:
                resolver = A2ACardResolver(client, url)
                card = await resolver.get_agent_card()
                self.remote_connections[card.name] = RemoteAgentConnection(card, url)
                self.cards[card.name] = card

    async def send_message(self, agent_name: str, task: str, tool_context: ToolContext):
        """Sends a message to a friend agent."""
        connection = self.remote_connections.get(agent_name)
        if not connection:
            raise ValueError(f"No such agent: {agent_name}")

        message_id = str(uuid.uuid4())
        payload = {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": task}],
                "messageId": message_id,
            }
        }

        request = SendMessageRequest(id=message_id, params=MessageSendParams.model_validate(payload))
        response = await connection.send_message(request)
        print(f"[INFO] Sent message to {agent_name}")
        return response

async def setup():
    # Define the friend agents our host should connect to.
    friend_urls = ["http://localhost:10004", "http://localhost:10005"]

    print("🌟 Starting up the Host Agent...")
    host = MilesAgent(remote_agent_urls=friend_urls)

    # Create the AI agent
    agent = await host.create_agent()
    print("✅ Host Agent is ready to coordinate meetings!")
    return agent
