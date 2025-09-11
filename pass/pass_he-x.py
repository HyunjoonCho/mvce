import argparse 
import json

LANGUAGES = ["java", "cpp", "go", "js", "python"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', default='gpt-4o')
    parser.add_argument('-r', default=10)
    args = parser.parse_args()
    
    
    for language in LANGUAGES:
        passed = dict()
        path = f"../results/HumanEval-X_{args.model}_base_{language}_results.jsonl"
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                result = json.loads(line)
                task_id = result["task_id"]
                if task_id not in passed:
                    passed[task_id] = 0
                passed[task_id] += 1 if result["passed"] else 0
        for key in passed:
            passed[key] /= 10
        output_path = f'pass_at_k/HumanEval-X_{language}_{args.model}@{args.r}.json'
        with open(output_path, 'w') as f:
            json.dump(passed, f, indent=4) 