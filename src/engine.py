import time
from abc import ABC
import json

import openai
import requests

class OllamaEngine(ABC):
    def __init__(self, model, endpoint):
        self._model = model
        self._base_url = endpoint

    def _extract_costs(self, response):
        return {
            key: response[key]
            for key in ['total_duration', 'load_duration', 'prompt_eval_count', 'prompt_eval_duration', 'eval_count', 'eval_duration']
            if key in response
        }

    def _query_model(self, payload):
        for _ in range(5):
            try:
                json_payload = json.dumps(payload)
                headers = {'Content-Type': 'application/json'}
                response = json.loads(requests.post(self._base_url, data=json_payload, headers=headers).text)
                costs = self._extract_costs(response)
                return response['response'], costs
            except Exception as e:
                save_err = e
                if "The server had an error processing your request." in str(e):
                    time.sleep(1)
                else:
                    break
        raise save_err

    def get_LLM_response(self, prompt):
        payload = {
            'model': self._model,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': 0.0,
                'num_predict': 500,
            },
        }
        return self._query_model(payload)

class OpenAIEngine(ABC):
    def __init__(self, model: str, api_key: str):
        self._model = model
        openai.api_key = api_key

    def _extract_costs(self, response):
        usage = response.usage
        return {
            'prompt_tokens': usage.prompt_tokens,
            'completion_tokens': usage.completion_tokens,
            'total_tokens': usage.total_tokens,
        }

    def _query_model(self, prompt: str):
        for _ in range(5):
            try:
                response = openai.chat.completions.create(
                    model=self._model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                    max_tokens=500
                )
                costs = self._extract_costs(response)
                reply = response.choices[0].message.content
                return reply, costs
            except Exception as e:
                save_err = e
                if "rate limit" in str(e).lower() or "server error" in str(e).lower():
                    time.sleep(1)
                else:
                    break
        raise save_err

    def get_LLM_response(self, prompt):
        return self._query_model(prompt)