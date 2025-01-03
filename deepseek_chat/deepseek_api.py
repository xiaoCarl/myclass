import requests
import json

class DeepSeekClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, message):
        payload = {
            "model": "deepseek-chat",
            "messages": [{
                "role": "user",
                "content": message
            }],
            "stream": True
        }
        
        try:
            with requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                stream=True
            ) as response:
                response.raise_for_status()
                # Process streaming response
                for line in response.iter_lines():
                    if line:
                        try:
                            # Remove 'data: ' prefix if present
                            if line.startswith(b'data: '):
                                line = line[6:]
                            
                            # Parse JSON
                            data = json.loads(line)
                            
                            # Extract content from different possible paths
                            if "choices" in data and len(data["choices"]) > 0:
                                # Try OpenAI-compatible format first
                                choice = data["choices"][0]
                                if "message" in choice:
                                    yield choice["message"]["content"]
                                elif "delta" in choice:
                                    yield choice["delta"]["content"]
                                elif "text" in choice:
                                    yield choice["text"]
                        except json.JSONDecodeError as e:
                           # print("JSON decode error:", e)
                            continue
        except requests.exceptions.RequestException as e:
            yield f"请求失败: {str(e)}"
