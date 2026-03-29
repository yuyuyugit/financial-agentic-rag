from enum import Enum
import os
import yaml
from openai import OpenAI


class QueryType(Enum):
    SIMPLE = "SIMPLE"
    COMPLEX = "COMPLEX"


class IntentRouter:
    def __init__(self, api_key: str = None, config_path: str = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "..", "config", "router_config.yaml")

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.simple_keywords = self.config["simple_keywords"]
        self.model = self.config["model"]
        self.max_tokens = self.config["max_tokens"]
        self.prompt_template = self.config["classification_prompt"]

    def route(self, query: str) -> QueryType:
        # Check for simple keywords
        if any(keyword in query for keyword in self.simple_keywords):
            return QueryType.SIMPLE

        # Use Qwen Flash to classify
        message = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": self.prompt_template.format(query=query)
                }
            ]
        )

        response_text = message.choices[0].message.content.strip().upper()
        return QueryType.SIMPLE if "SIMPLE" in response_text else QueryType.COMPLEX
