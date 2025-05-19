#!/bin/bash

run_pass() {
  result_file="$1"
  for i in $(seq 1 20); do
    python pass.py -r "$result_file" -k "$i"
  done
}

run_pass ../results/HumanEval_llama3.json
run_pass ../results/HumanEval_llama3.1.json
run_pass ../results/HumanEval_mistral-nemo.json
run_pass ../results/HumanEval_qwen2.5-coder.json