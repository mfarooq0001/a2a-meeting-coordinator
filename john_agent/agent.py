# John Agent Implementation

from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv
import os

load_dotenv()

class JohnAgent():
    CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
    self.api_key = = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment")

    self.llm = LLM(
        model = "gemini/gemini-2.0-flash"
        api_key = api_key,
    )

    self.agent = Agent(
        role = "Scheduling agent",
        goal = "You are John's assitant, an advanced AI assistant designed to help schedule meetings for Mr. John. Use the provided tools to assist with scheduling and managing appointments efficiently.",
        backstory = "You can answer scheduling questions and you always use the calendar tool",
        tools = [AvailabilityTool()],
        llm = self.llm,
    )

    async def invoke(self, user_question):
        try:
            task = Task(
                description = f"Respond to this question {user_question}",
                expected_output = "Clear answer about John's availablilty",
                agent = self.agent
            )
            crew = Crew(
                agents = [self.agent],
                tasks = [task],
                process = Process.sequential
            )

            result = crew.kickoff()
            return str(result) if result else "No response available"
        except Exception as e:
            print(f"[ERROR] john_agent.invoke: {e}")
            return f"Sorry, I encountered an error: {str(e)}"