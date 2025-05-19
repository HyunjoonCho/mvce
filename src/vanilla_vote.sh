#!/bin/bash

python vote.py -r ../results/HumanEval_llama3.json
python vote.py -r ../results/HumanEval_llama3.1.json
python vote.py -r ../results/HumanEval_mistral-nemo.json
python vote.py -r ../results/HumanEval_qwen2.5-coder.json