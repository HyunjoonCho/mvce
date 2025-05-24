import argparse
import json
import random
import os
import numpy as np

#import tqdm

def get_entropy(data):
    probs = np.array(data).astype(float)
    probs = probs / np.sum(probs)
    entropy = -np.sum(probs * np.log2(probs))
    return entropy

def vote_by_majority(responses):
    votes = dict()
    passed = dict()
    
    for response in responses:
        source = response[0]
        source = '\n'.join(
            [
                line for line in source.split('\n') 
                if not line.startswith('```') and not line.strip().startswith('def ')
            ])
        if source not in votes:
            passed[source] = response[1]['result'] == "passed"
            votes[source] = 0
        votes[source] += 1
    
    max_votes = max(votes.values())
    entropy = get_entropy(list(votes.values()))
    top_sources = [src for src, count in votes.items() if count == max_votes]
    chosen_source = random.choice(top_sources)
    
    return chosen_source, max_votes, passed[chosen_source], entropy

def decompose_name(name):
    if name.endswith('.json'):
        name = name[:-5]
    if name.endswith('_instruction'):
        name = name[:-12]
        mode = 'instruction'
    elif name.endswith('_rule'):
        name = name[:-5]
        mode = 'rule'
    else:
        mode = 'default'
    if name.endswith('_qwen2.5-coder'):
        name = name[:-14]
        model = 'qwen2.5-coder'
    elif name.endswith('_mistral-nemo'):
        name = name[:-13]
        model = 'mistral-nemo'
    elif name.endswith('_llama3'):
        name = name[:-7]
        model = 'llama3'
    elif name.endswith('_llama3.1'):
        name = name[:-9]
        model = 'llama3.1'
    if name.endswith('APPS'):
        name = name[:-4]
        dataset = 'APPS'
    elif name.endswith('HumanEval'):
        name = name[:-9]
        dataset = 'HumanEval'
    
    return dataset, model, mode

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--responses_path', default='../results/HumanEval_llama3.json')
    args = parser.parse_args()

    if args.responses_path.endswith('\r'):
        args.responses_path = args.responses_path[:-1]
    
    with open(args.responses_path) as f:
        benchmark_responses = json.load(f)
    
    passed_count = 0
    entropy = []
    for id in benchmark_responses:
        source, votes, is_passed, entr = vote_by_majority(benchmark_responses[id])
        entropy.append(entr)
        passed_count += int(is_passed)

    model, mode, dataset = decompose_name(args.responses_path)
    results_to_save = {
        'model': model,
        'mode': mode,
        'dataset': dataset,
        'passed_count': passed_count,
        'total_count': len(benchmark_responses),
        'entropy': np.mean(entropy),
    }
    output_path = '../results/entropy/majority_vote_results.json'
    try:
        with open(output_path, 'r') as f:
            existing_results = json.load(f)
    except:
        existing_results = {}
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    existing_results[args.responses_path] = results_to_save
    with open(output_path, 'w') as f:
        json.dump(existing_results, f, indent=4)

    print(f"For {args.responses_path}, {passed_count} ranked at top correctly")