from enum import Enum
import os
import yaml
import anthropic


class QueryType(Enum):
    SIMPLE = "SIMPLE"
    COMPLEX = "COMPLEX"


class IntentRouter:
    def __init__(self, api_key: str = None, config_path: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key)

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

        # Use Claude Haiku to classify
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": self.prompt_template.format(query=query)
                }
            ]
        )

        response_text = message.content[0].text.strip().upper()
        return QueryType.SIMPLE if "SIMPLE" in response_text else QueryType.COMPLEX
