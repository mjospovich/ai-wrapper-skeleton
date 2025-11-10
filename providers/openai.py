"""
OpenAI Provider Implementation

This is an example provider implementation. To add a new provider:
1. Copy this file and modify the class name and API calls
2. Import the new class in providers/__init__.py
3. Add it to the provider_map in main.py
"""

from openai import OpenAI
from .base import BaseAIClient

class OpenAIClient(BaseAIClient):
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content