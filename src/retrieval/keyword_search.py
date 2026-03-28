import yaml
from pathlib import Path


class KeywordSearcher:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "keyword_search_config.yaml"

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.mock_data = config.get('mock_data', {})

    def search(self, query: str) -> dict:
        for key, value in self.mock_data.items():
            if key in query:
                return {"result": value, "source": "keyword_search"}
        return {"result": "未找到相关信息", "source": "keyword_search"}
