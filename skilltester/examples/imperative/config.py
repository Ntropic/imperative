from nooa.unifiedllm import CompletionClient


llm = CompletionClient(
    model="openai/inkling2:mini-nvfp4-pruned@dspark-offload-cpu-vision",
    base_url="http://192.168.178.123:8000/v1",
    api_key="local",
)

# Or use separate clients:
# llm = {
#     "candidate": CompletionClient(...),
#     "judge": CompletionClient(...),
# }
