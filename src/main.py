from autogen_core import (
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    TopicId,
    message_handler,
    type_subscription,
)

from autogen_core.tool_agent import ToolAgent
from autogen_core.tools import FunctionTool, Tool
from typing import List

from src.utils.topic_type import z_agent_topic_type, user_topic_type
from src.utils.data_class import Message
from src.z_agent import ZAgent
from src.utils.model_clients import openai_model_client, openai_model_client_o4_mini
from src.utils.tools import get_archaeological_sites
from src.utils.prompts import z_agent_prompt_v2, z_agent_prompt_v1
import asyncio


@type_subscription(topic_type=user_topic_type)
class UserAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("A user agent that output messages to the user topic")

    @message_handler
    async def handle_message(self, message:Message, ctx: MessageContext) -> None:
        """
        Handle incoming messages from the user topic.
        This method processes messages directed to the user agent and can be extended
        to perform actions based on the content of the messages.
        Args:
            message (Message): The incoming message to process.
            ctx (MessageContext): The context of the message, providing additional information.
        """
        # Here you can implement logic to handle the message
        # For example, you might want to log the message or perform some action based on its content
        print(f"Received message: {message.content} in context: {ctx}")


async def main():
    """
    Main function to run the UserAgent.
    This function initializes the UserAgent and starts its runtime.
    """
    runtime = SingleThreadedAgentRuntime()

    
    z_agent_tools: List[Tool] = [
        FunctionTool(
            get_archaeological_sites,
            description="Get a list of potential archaeological sites based on the provided location.",
        )
    ]

    # Register the z_agent_tools with ToolAgent
    await ToolAgent.register(
        runtime,
        "z_agent_tool_agent",
        lambda: ToolAgent("z_agent_tool_agent", z_agent_tools),
    )

    # z_agent_tools: List[Tool] = []

    await ZAgent.register(runtime, type=z_agent_topic_type, factory=lambda: ZAgent(openai_model_client_o4_mini, [tool.schema for tool in z_agent_tools], "z_agent_tool_agent"))
    await UserAgent.register(runtime, type=user_topic_type, factory=lambda: UserAgent())

    # Start the runtime to process messages
    runtime.start()

    await runtime.publish_message(
        topic_id=TopicId(z_agent_topic_type, source="user"),
        message=Message(content=z_agent_prompt_v2),
    )

    await runtime.stop_when_idle()

    return None


if __name__ == "__main__":
    asyncio.run(main())


