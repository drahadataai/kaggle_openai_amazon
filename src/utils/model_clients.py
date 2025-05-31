from autogen_ext.models.openai import OpenAIChatCompletionClient

openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key="#########",
    max_retries=3,
    retry_delay=2,
    timeout=30,
)


openai_model_client_o4_mini = OpenAIChatCompletionClient(
    model="o4-mini",
    api_key="########",
    max_retries=3,
    retry_delay=2,
    timeout=30,
)