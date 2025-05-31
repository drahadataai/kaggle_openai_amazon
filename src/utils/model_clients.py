from autogen_ext.models.openai import OpenAIChatCompletionClient

openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key="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",
    max_retries=3,
    retry_delay=2,
    timeout=30,
)


openai_model_client_o4_mini = OpenAIChatCompletionClient(
    model="o4-mini",
    api_key="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",
    max_retries=3,
    retry_delay=2,
    timeout=30,
)