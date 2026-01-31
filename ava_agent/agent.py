# Ava Agent Implementation (Langchain)

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenenerativeAI
from langchain_core.messages.ai import AIMessage
from langgraph.checkpointer import MemorySaver
from dotenv import load_dotenv
from tools import check_ava_availability

# Load environment variables from .env file
load_dotenv()

# Memory
memory = MemorySaver()

class AvaAgent():

    # Content types
    CONTENT_TYPES = ["text", "text/plain"]
    
    def __init__(self):
        self.model = ChatGoogleGenenerativeAI(model="gemini-2.0-flash")
        self.tools = [check_ava_availability]
        self.system_prompt = "You are Ava, an advanced AI assistant designed to help schedule meetings for Ms. Ava Smith. Use the provided tools to assist with scheduling and managing appointments efficiently."

        self.graph = create_agent(
            model=self.model, 
            tools=self.tools, 
            system_prompt=self.system_prompt,
            checkpointer=memory,
        )

    async def get_response(self, query, context_id):
        inputs = {"messages": [{"user": query}]}
        config = {"configurable": {"thread_id": context_id}}
        raw_response = await self.graph.invoke(inputs, config)
        messages = raw_response['messages', []]
        ai_message = [message.content for message in messages if isinstance(message, AIMessage)]
        response = ai_message[0] if ai_message else "I'm sorry, I couldn't process your request."
        return response

