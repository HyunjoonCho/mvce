#!/bin/bash

python vote.py -r ../results/HumanEval_llama3.json
python vote.py -r ../results/HumanEval_llama3.1.json
python vote.py -r ../results/HumanEval_mistral-nemo.json
python vote.py -r ../results/HumanEval_qwen2.5-coder.json

python vote.py -r ../results/HumanEval_llama3_instruction.json
python vote.py -r ../results/HumanEval_llama3.1_instruction.json
python vote.py -r ../results/HumanEval_mistral-nemo_instruction.json
python vote.py -r ../results/HumanEval_qwen2.5-coder_instruction.json

python vote.py -r ../results/HumanEval_llama3_rule.json
python vote.py -r ../results/HumanEval_llama3.1_rule.json
python vote.py -r ../results/HumanEval_mistral-nemo_rule.json
python vote.py -r ../results/HumanEval_qwen2.5-coder_rule.json

python vote.py -r ../results/APPS_llama3.json
python vote.py -r ../results/APPS_llama3.1.json
python vote.py -r ../results/APPS_mistral-nemo.json
python vote.py -r ../results/APPS_qwen2.5-coder.json

python vote.py -r ../results/APPS_llama3_instruction.json
python vote.py -r ../results/APPS_llama3.1_instruction.json
python vote.py -r ../results/APPS_mistral-nemo_instruction.json
python vote.py -r ../results/APPS_qwen2.5-coder_instruction.json

python vote.py -r ../results/APPS_llama3_rule.json
python vote.py -r ../results/APPS_llama3.1_rule.json
python vote.py -r ../results/APPS_mistral-nemo_rule.json
python vote.py -r ../results/APPS_qwen2.5-coder_rule.json