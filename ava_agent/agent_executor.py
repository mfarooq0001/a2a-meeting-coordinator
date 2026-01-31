# Agent Executor for AVA Agent

from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from agent import AvaAgent

class AvaAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = AvaAgent()

    async def execute(self, request_context: RequestContext, event_queue: EventQueue):
        query = request_context.query
        context_id = request_context.context_id

        response = await self.agent.get_response(query, context_id)

        return response

    async def cancel(self, request_context: RequestContext):
        # Cancellation logic
        pass