from autogen_core import (
    MessageContext,
    TopicId,
    AgentId,
    message_handler,
    type_subscription,

)

from autogen_core.tool_agent import tool_agent_caller_loop, ToolAgent
from autogen_core.tools import FunctionTool, Tool, ToolSchema

from src.utils.model_clients import openai_model_client, openai_model_client_o4_mini
from src.utils.topic_type import z_agent_topic_type, user_topic_type

from autogen_core.models import (
    ChatCompletionClient,
    SystemMessage,
    UserMessage,
    LLMMessage,
)

from typing import List, Dict, Any
from src.utils.data_class import Message
from src.utils.prompts import z_agent_prompt_v2
from autogen_core import RoutedAgent, AgentId

@type_subscription(topic_type=z_agent_topic_type)
class ZAgent(RoutedAgent):
    """An agent that uses tools to perform tasks. It executes the tools
    by itself by sending the tool execution task to a ToolAgent."""

    def __init__(
        self,
        model_client: ChatCompletionClient,
        tool_schema: List[ToolSchema],
        tool_agent_type: str,
    ) -> None:
        super().__init__("An agent that interacts with the Z topic and uses tools")
        self._model_client = model_client
        self._system_messages: List[LLMMessage] = [
            SystemMessage(
                content=z_agent_prompt_v2
            )
        ]
        self._tool_schema = tool_schema
        self._tool_agent_id = AgentId(type=tool_agent_type, key=self.id.key)

    @message_handler
    async def handle_user_message(self, message: Message, ctx: MessageContext) -> None:
        """Handle a user message, execute the model and tools, and returns the response."""
        session: List[LLMMessage] = [UserMessage(content=message.content, source="User")]
        # Use the tool agent to execute the tools, and get the output messages.
        output_messages = await tool_agent_caller_loop(
            self,
            tool_agent_id=self._tool_agent_id,
            model_client=self._model_client,
            input_messages=session,
            tool_schema=self._tool_schema,
            cancellation_token=ctx.cancellation_token,
        )
        # Extract the final response from the output messages.
        final_response = output_messages[-1].content
        assert isinstance(final_response, str)
        
        print(f"ZAgent response: {final_response}")

        await self.publish_message(
            topic_id=TopicId(type=user_topic_type, source=self.id.key),
            message=Message(content=final_response),
        )