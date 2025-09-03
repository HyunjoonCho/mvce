import argparse
import json
import os
import re

def process_generated_codes(generated_codes):
    per_language_results = dict()
    
    for task_id, responses in generated_codes.items():
        language = task_id.split('/')[0]
        
        if language not in per_language_results:
            per_language_results[language] = []
        
        for response in responses:
            code = response[0]
            
            code = re.sub(r'^```\w*\n?', '', code)
            code = re.sub(r'\n?```$', '', code)

            if language == 'Java':
                open_braces = code.count('{')
                close_braces = code.count('}')
                
                required_closing_braces = open_braces + 2
                
                if close_braces < required_closing_braces:
                    missing_braces = required_closing_braces - close_braces
                    code += "\n" + "}" * missing_braces
            
            lines = code.split('\n')
            if lines and any(keyword in lines[0].lower() for keyword in ['function', 'def ', 'func ', 'int ', 'void ']):
                code = '\n'.join(lines[1:])
            
            per_language_results[language].append({
                "task_id": task_id,
                "generation": code
            })
    
    return per_language_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--benchmark', default='HumanEval-X', choices=['HumanEval-X'])
    parser.add_argument('-r', '--responses_path', default='../results/HumanEval-X_gpt-4o_base.json')
    args = parser.parse_args()
    
    with open(args.responses_path) as f:
        data = json.load(f)
    per_language_results = process_generated_codes(data)
    
    for language in per_language_results:
        output_path = args.responses_path.replace('.json', f'_{language.lower() if language != "JavaScript" else "js"}.jsonl')
        with open(output_path, 'w') as f:
            for result in per_language_results[language]:
                f.write(json.dumps(result) + "\n")