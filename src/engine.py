import time
from abc import ABC
import json

import openai
import requests
import google.generativeai as genai
from google.generativeai import GenerationConfig
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class HFEngine(ABC):
    def __init__(self, model):
        self._model = AutoModelForCausalLM.from_pretrained(model, torch_dtype=torch.bfloat16, trust_remote_code=True, device_map='auto')
        self._tokenizer = AutoTokenizer.from_pretrained(model, torch_dtype=torch.bfloat16, trust_remote_code=True, device_map='auto')
        self._generator = pipeline("text-generation", model=self._model, tokenizer=self._tokenizer, torch_dtype=torch.bfloat16, device_map='auto')

    def _extract_costs(self, prompt, generated_code):
        return {
            'prompt_tokens': len(self._tokenizer.encode(prompt)), 
            'completion_tokens': len(self._tokenizer.encode(generated_code)), 
        }

    def _query_model(self, prompt):
        for _ in range(5):
            try:
                messages = [{"role": "user", "content": prompt}]
                prompt = self._tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                response = self._generator(prompt, temperature=1e-5, return_full_text=False)
                generated_code = response[0]['generated_text']
                costs = self._extract_costs(prompt, generated_code)
                return generated_code, costs
            except Exception as e:
                save_err = e
                if "The server had an error processing your request." in str(e):
                    time.sleep(1)
                else:
                    break
        raise save_err

    def get_LLM_response(self, prompt):
        return self._query_model(prompt)

class OllamaEngine(ABC):
    def __init__(self, model, endpoint):
        self._model = model
        self._base_url = endpoint

    def _extract_costs(self, response):
        return {
            'prompt_tokens': response['prompt_eval_count'],
            'completion_tokens': response['eval_count'],
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

class GeminiEngine(ABC):
    def __init__(self, model: str, api_key: str):
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model)
        self._generation_config = GenerationConfig(
            candidate_count=1,
            temperature=0.0,
            max_output_tokens=2048,
        )

    def _extract_costs(self, response):
        usage = response.usage_metadata
        return {
            'prompt_tokens': usage.prompt_token_count,
            'completion_tokens': usage.candidates_token_count,
        }
        
    def _query_model(self, prompt: str):
        for _ in range(5):
            try:
                response = self._model.generate_content(
                    prompt,
                    generation_config=self._generation_config,
                )
                if response.candidates[0].finish_reason == 1 or response.candidates[0].finish_reason == 2:
                    costs = self._extract_costs(response)
                    reply = response.text
                    return reply, costs
                else:
                    save_err = Exception(f"Finish reason was not 1 nor 2: {response.candidates[0].finish_reason}")
                    time.sleep(1)
                    continue
            except Exception as e:
                save_err = e
                error_str = str(e).lower()
                if any(keyword in error_str for keyword in ["rate limit", "quota", "server error", "service unavailable", "timeout"]):
                    time.sleep(1)
                else:
                    break
        raise save_err

    def get_LLM_response(self, prompt):
        return self._query_model(prompt)
