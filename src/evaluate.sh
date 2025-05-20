#!/bin/bash

python evaluator.py -b HumanEval -r ../results/HumanEval_llama3_instruction.json
python evaluator.py -b HumanEval -r ../results/HumanEval_llama3_rule.json
python evaluator.py -b HumanEval -r ../results/HumanEval_llama3.1_instruction.json
python evaluator.py -b HumanEval -r ../results/HumanEval_llama3.1_rule.json
python evaluator.py -b HumanEval -r ../results/HumanEval_mistral-nemo_instruction.json
python evaluator.py -b HumanEval -r ../results/HumanEval_mistral-nemo_rule.json
python evaluator.py -b HumanEval -r ../results/HumanEval_qwen2.5-coder_instruction.json
python evaluator.py -b HumanEval -r ../results/HumanEval_qwen2.5-coder_rule.json

python evaluator.py -b APPS -r ../results/APPS_llama3_instruction.json
python evaluator.py -b APPS -r ../results/APPS_llama3_rule.json
python evaluator.py -b APPS -r ../results/APPS_llama3.1_instruction.json
python evaluator.py -b APPS -r ../results/APPS_llama3.1_rule.json
python evaluator.py -b APPS -r ../results/APPS_mistral-nemo_instruction.json
python evaluator.py -b APPS -r ../results/APPS_mistral-nemo_rule.json
python evaluator.py -b APPS -r ../results/APPS_qwen2.5-coder_instruction.json
python evaluator.py -b APPS -r ../results/APPS_qwen2.5-coder_rule.json
