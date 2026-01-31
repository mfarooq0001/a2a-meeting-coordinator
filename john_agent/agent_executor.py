# Agent Executor for John Agent

from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Part, TextPart

from agent import JohnAgent

class JohnAgentExecutor(AgentExecutor):

    def __init__(self):
        self.agent = JohnAgent()

    async def execute(self, request_context: RequestContext, event_queue: EventQueue):
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)

        if not context.current_task:
            await updater.submit()
        await updater.start_work()

        query = context.get_user_input()

        response = await self.agent.invoke(user_question=query)
        parts = [Part(root=TextPart(text=response))]

        await updater.add_artifact(parts, name="scheduling_result")
        await updater.complete()

      async def cancel(self, context: RequestContext, event_queue: EventQueue):
        return


