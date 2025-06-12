from vllm import LLM

class VLLMClient:
    def __init__(self, model_id: str, gpu_ids: list[int] = [0], max_gpu_mem_mb: int = 80000):
        self.llm = LLM(model=model_id, gpu_ids=gpu_ids, max_gpu_mem_mb=max_gpu_mem_mb)

    async def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        response = await self.llm.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.generated_text
