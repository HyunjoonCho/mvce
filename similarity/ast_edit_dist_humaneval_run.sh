#!/bin/bash

# without preprocessing
output_file="./ast_edit_dist_humaneval_wo_preprocessing_results.txt"
echo "" > "$output_file"

result_paths=(
    '../preprocessed_results/ast_only/HumanEval_llama3.json'
    '../preprocessed_results/ast_only/HumanEval_llama3.1.json'
    '../preprocessed_results/ast_only/HumanEval_mistral-nemo.json'
    '../preprocessed_results/ast_only/HumanEval_qwen2.5-coder.json'
    '../preprocessed_results/ast_only/HumanEval_llama3_rule.json'
    '../preprocessed_results/ast_only/HumanEval_llama3.1_rule.json'
    '../preprocessed_results/ast_only/HumanEval_mistral-nemo_rule.json'
    '../preprocessed_results/ast_only/HumanEval_qwen2.5-coder_rule.json'
    '../preprocessed_results/ast_only/HumanEval_llama3_instruction.json'
    '../preprocessed_results/ast_only/HumanEval_llama3.1_instruction.json'
    '../preprocessed_results/ast_only/HumanEval_mistral-nemo_instruction.json'
    '../preprocessed_results/ast_only/HumanEval_qwen2.5-coder_instruction.json'
)

for result_path in "${result_paths[@]}"; do
    echo "$result_path" >> "$output_file"
    echo "python ast_similarity.py -b HumanEval -r $result_path"
    output=$(python ast_similarity.py -b HumanEval -r "$result_path")
    num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
    num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
    echo "num_passed: $num_passed" >> "$output_file"
    echo "num_total: $num_total" >> "$output_file"
    echo "===============================================" >> "$output_file"
done

# echo "Running with llama3..."
# output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_llama3.json)
# num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# echo "[llama3]" >> "$output_file"
# echo "num_passed: $num_passed" >> "$output_file"
# echo "num_total: $num_total" >> "$output_file"
# echo "===============================================" >> "$output_file"


# echo "Running with llama3.1..."
# output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_llama3.1.json)
# num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# echo "[llama3.1]" >> "$output_file"
# echo "num_passed: $num_passed" >> "$output_file"
# echo "num_total: $num_total" >> "$output_file"
# echo "===============================================" >> "$output_file"

# echo "Running with mistral-nemo..."
# output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_mistral-nemo.json)
# num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# echo "[mistral-nemo]" >> "$output_file"
# echo "num_passed: $num_passed" >> "$output_file"
# echo "num_total: $num_total" >> "$output_file"
# echo "===============================================" >> "$output_file"

# echo "Running with qwen2.5-coder..."
# output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_qwen2.5-coder.json)
# num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# echo "[qwen2.5-coder]" >> "$output_file"
# echo "num_passed: $num_passed" >> "$output_file"
# echo "num_total: $num_total" >> "$output_file"
# echo "===============================================" >> "$output_file"

# # echo "Running with llama3_instruction..."
# # output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_llama3_instruction.json)
# # num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# # num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# # echo "[llama3_instruction]" >> "$output_file"
# # echo "num_passed: $num_passed" >> "$output_file"
# # echo "num_total: $num_total" >> "$output_file"
# # echo "===============================================" >> "$output_file"

# # echo "Running with llama3.1_instruction..."
# # output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_llama3.1_instruction.json)
# # num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# # num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# # echo "[llama3.1_instruction]" >> "$output_file"
# # echo "num_passed: $num_passed" >> "$output_file"
# # echo "num_total: $num_total" >> "$output_file"
# # echo "===============================================" >> "$output_file"

# # echo "Running with mistral-nemo_instruction..."
# # output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_mistral-nemo_instruction.json)
# # num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# # num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# # echo "[mistral-nemo_instruction]" >> "$output_file"
# # echo "num_passed: $num_passed" >> "$output_file"
# # echo "num_total: $num_total" >> "$output_file"
# # echo "===============================================" >> "$output_file"

# # echo "Running with qwen2.5-coder_instruction..."
# # output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_qwen2.5-coder_instruction.json)
# # num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# # num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# # echo "[qwen2.5-coder_instruction]" >> "$output_file"
# # echo "num_passed: $num_passed" >> "$output_file"
# # echo "num_total: $num_total" >> "$output_file"
# # echo "===============================================" >> "$output_file"

# # echo "Running with llama3_rule..."
# # output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_llama3_rule.json)
# # num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# # num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# # echo "[llama3_rule]" >> "$output_file"
# # echo "num_passed: $num_passed" >> "$output_file"
# # echo "num_total: $num_total" >> "$output_file"
# # echo "===============================================" >> "$output_file"

# # echo "Running with llama3.1_rule..."
# # output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_llama3.1_rule.json)
# # num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# # num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# # echo "[llama3.1_rule]" >> "$output_file"
# # echo "num_passed: $num_passed" >> "$output_file"
# # echo "num_total: $num_total" >> "$output_file"
# # echo "===============================================" >> "$output_file"

# # echo "Running with mistral-nemo_rule..."
# # output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_mistral-nemo_rule.json)
# # num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# # num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# # echo "[mistral-nemo_rule]" >> "$output_file"
# # echo "num_passed: $num_passed" >> "$output_file"
# # echo "num_total: $num_total" >> "$output_file"
# # echo "===============================================" >> "$output_file"

# # echo "Running with qwen2.5-coder_rule..."
# # output=$(python ast_similarity.py -b HumanEval -r ../preprocessed_results/ast_only/HumanEval_qwen2.5-coder_rule.json)
# # num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
# # num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
# # echo "[qwen2.5-coder_rule]" >> "$output_file"
# # echo "num_passed: $num_passed" >> "$output_file"
# # echo "num_total: $num_total" >> "$output_file"
# # echo "===============================================" >> "$output_file"


