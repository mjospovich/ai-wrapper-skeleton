from .base import BaseAIClient
from anthropic import Anthropic

class AnthropicClient(BaseAIClient):
    def __init__(self, api_key: str, model: str):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate_response(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text