import argparse
import json

def pass_at_k(responses, k=20):
    assert k <= len(responses)

    for response in responses[:k]:
        if response[1]['result'] == "passed":
            return True

    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--responses_path', default='../results/HumanEval_llama3.json')
    parser.add_argument('-k', default="20")
    args = parser.parse_args()
    
    with open(args.responses_path) as f:
        benchmark_responses = json.load(f)
    
    passed = dict()
    for id in benchmark_responses:
        is_passed = pass_at_k(benchmark_responses[id], int(args.k))
        passed[id] = is_passed
    
    output_path = args.responses_path.replace('../results', f'./pass_at_k/').replace('.json', f'@{args.k}.json')
    with open(output_path, 'w') as f:
        json.dump(passed, f, indent=4) 
    
    print(f"For {args.responses_path}, pass@{args.k}: {len([t for t in passed.values() if t])}")