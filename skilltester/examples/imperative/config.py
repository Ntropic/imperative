from nooa.unifiedllm import CompletionClient


llm = CompletionClient(
    model="openai/qwen3.6:27b-pruned",
    base_url="http://192.168.178.123:8000/v1",
    api_key="local",
)

# Or use separate clients:
# llm = {
#     "candidate": CompletionClient(...),
#     "judge": CompletionClient(...),
# }
