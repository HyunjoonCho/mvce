#!/bin/bash

python evaluator.py -b HumanEval -r ../results/HumanEval_Meta-Llama-3-8B-Instruct_base.json
python evaluator.py -b HumanEval -r ../results/HumanEval_Meta-Llama-3.1-8B-Instruct_base.json
python evaluator.py -b HumanEval -r ../results/HumanEval_Mistral-Nemo-Instruct-2407_base.json
python evaluator.py -b HumanEval -r ../results/HumanEval_Qwen2.5-Coder-7B-Instruct_base.json
python evaluator.py -b HumanEval -r ../results/HumanEval_phi-4_base.json
# python evaluator.py -b HumanEval -r ../results/HumanEval_gpt-4o_base.json
# python evaluator.py -b HumanEval -r ../results/HumanEval_gemini-2.5-flash-lite_base.json

python evaluator.py -b APPS -r ../results/APPS_Meta-Llama-3-8B-Instruct_base.json
python evaluator.py -b APPS -r ../results/APPS_Meta-Llama-3.1-8B-Instruct_base.json
python evaluator.py -b APPS -r ../results/APPS_Mistral-Nemo-Instruct-2407_base.json
python evaluator.py -b APPS -r ../results/APPS_Qwen2.5-Coder-7B-Instruct_base.json
python evaluator.py -b APPS -r ../results/APPS_phi-4_base.json
# python evaluator.py -b APPS -r ../results/APPS_gpt-4o_base.json
# python evaluator.py -b APPS -r ../results/APPS_gemini-2.5-flash-lite_base.json
