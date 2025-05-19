import argparse
import json
import random

import tqdm

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
    top_sources = [src for src, count in votes.items() if count == max_votes]
    chosen_source = random.choice(top_sources)
    
    return chosen_source, max_votes, passed[chosen_source]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--responses_path', default='../results/HumanEval_llama3.json')
    args = parser.parse_args()
    
    with open(args.responses_path) as f:
        benchmark_responses = json.load(f)
    
    passed_count = 0
    for id in tqdm.tqdm(benchmark_responses):
        source, votes, is_passed = vote_by_majority(benchmark_responses[id])
        if is_passed:
            passed_count += 1
    print(f"For {args.responses_path}, {passed_count} ranked at top correctly")