# actual querying and storing; measure time, in-out tokens - engine.py + parser.py
import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm

from engine import OllamaEngine, OpenAIEngine, GeminiEngine

DEFAULT_OLLAMA_ENDPOINT = 'http://localhost:11434/api/generate'

class BaseCodeGenerator:
    def __init__(self, R=3):
        self.number_of_repetitions = R
    
    def query_model(self, problem):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.get_LLM_response, problem) for _ in range(self.number_of_repetitions)]
            results = []
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    print(f"Error during query: {e}")
        return results

class OllamaCodeGenerator(OllamaEngine, BaseCodeGenerator):
    def __init__(self, model, endpoint, R=3):
        OllamaEngine.__init__(self, model, endpoint)
        BaseCodeGenerator.__init__(self, R)

class OpenAICodeGenerator(OpenAIEngine, BaseCodeGenerator):
    def __init__(self, model, api_key, R=3):
        OpenAIEngine.__init__(self, model, api_key)
        BaseCodeGenerator.__init__(self, R)

class GeminiCodeGenerator(GeminiEngine, BaseCodeGenerator):
    def __init__(self, model, api_key, R=3):
        GeminiEngine.__init__(self, model, api_key)
        BaseCodeGenerator.__init__(self, R)

def get_code_generator(model, R=3):
    if model.startswith('gpt'):
        return OpenAICodeGenerator(model, os.environ['OPENAI_API_KEY'], R)
    elif model.startswith('models/gemini'):
        return GeminiCodeGenerator(model, os.environ['GOOGLE_API_KEY'], R)
    else:
        return OllamaCodeGenerator(model, DEFAULT_OLLAMA_ENDPOINT, R)

def format_prompt(benchmark, template, samples, id, key):
    if benchmark == "HumanEval-X":
        return [(sample[id], template.format(problem=sample[key], language=sample[id].split('/')[0])) for sample in samples]
    else:
        return [(sample[id], template.format(problem=sample[key])) for sample in samples]

def load_benchmark(benchmark, prompt_type):
    data_path = f"../data/{benchmark}.jsonl"
    prompt_path = f"../prompt/{benchmark}_{prompt_type}.txt"
    if benchmark == "HumanEval" or benchmark == "HumanEval-X":
        id, key = "task_id", "prompt"
    else:
        id, key = "id", "question"
        
    with open(data_path) as f:
        data = [json.loads(line) for line in f]
    with open(prompt_path) as f:
        template = f.read()
    
    return format_prompt(benchmark, template, data, id, key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', default='gpt-4o')
    parser.add_argument('-b', '--benchmark', default='HumanEval-X')
    parser.add_argument('-p', '--prompt', default='base')
    parser.add_argument('-o', '--output_dir', default='../results')
    parser.add_argument('-r', '--runs', default="10")
    args = parser.parse_args()
    assert args.benchmark in ["HumanEval", "APPS", "HumanEval-X"]
    assert args.prompt in ["base", "instruction", "rule"]
    os.makedirs(args.output_dir, exist_ok=True)
    
    model = args.model.split('/')[-1] # handle Gemini-specific model naming convention
    result_path = os.path.join('../results', f'{args.benchmark}_{model}_{args.prompt}.json')
    if os.path.isfile(result_path):
        with open(result_path) as f:
            result_dict = json.load(f)
    else:
        result_dict = dict()
    
    benchmark = load_benchmark(args.benchmark, args.prompt)
    
    generator = get_code_generator(args.model, R=int(args.runs))

    for id, problem in tqdm.tqdm(benchmark):
        id = str(id)
        if id in result_dict and len(result_dict[id]) == int(args.runs):
            continue
        else:
            result = generator.query_model(problem)
            result_dict[id] = result
            with open(result_path, 'w') as f:
                json.dump(result_dict, f, indent=4)
   
