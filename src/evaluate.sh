#!/bin/bash

# python evaluator.py -b HumanEval -r ../results/HumanEval_llama3_base.json
# python evaluator.py -b HumanEval -r ../results/HumanEval_llama3.1_base.json
# python evaluator.py -b HumanEval -r ../results/HumanEval_mistral-nemo_base.json
# python evaluator.py -b HumanEval -r ../results/HumanEval_qwen2.5-coder_base.json
python evaluator.py -b HumanEval -r ../results/HumanEval_phi4_base.json
# python evaluator.py -b HumanEval -r ../results/HumanEval_gpt-4o_base.json

# python evaluator.py -b APPS -r ../results/APPS_llama3_base.json
# python evaluator.py -b APPS -r ../results/APPS_llama3.1_base.json
# python evaluator.py -b APPS -r ../results/APPS_mistral-nemo_base.json
# python evaluator.py -b APPS -r ../results/APPS_qwen2.5-coder_base.json
python evaluator.py -b APPS -r ../results/APPS_phi4_base.json
# python evaluator.py -b APPS -r ../results/APPS_gpt-4o_base.json
