#!/bin/bash

output_file="./codebert_kmean_apps_results.txt"
echo "" > "$output_file"

num_clusters=(10)
result_paths=(
    '../results/APPS_llama3.json'
    '../results/APPS_llama3.1.json'
    '../results/APPS_mistral-nemo.json'
    '../results/APPS_qwen2.5-coder.json'
    '../results/APPS_llama3_rule.json'
    '../results/APPS_llama3.1_rule.json'
    '../results/APPS_mistral-nemo_rule.json'
    '../results/APPS_qwen2.5-coder_rule.json'
)

for result_path in "${result_paths[@]}"; do
    echo "$result_path" >> "$output_file"
    for num_cluster in "${num_clusters[@]}"; do
        echo "[Num_cluster = $num_cluster]" >> "$output_file"
        echo "python codebert_kmean.py -b APPS -r $result_path -n $num_cluster"
        output=$(python codebert_kmean.py -b APPS -r "$result_path" -n "$num_cluster")
        num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
        num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
        echo "num_passed: $num_passed" >> "$output_file"
        echo "num_total: $num_total" >> "$output_file"
        echo "===============================================" >> "$output_file"
    done
done

num_clusters=(5)
result_paths=(
    '../results/APPS_llama3_instruction.json'
    '../results/APPS_llama3.1_instruction.json'
    '../results/APPS_mistral-nemo_instruction.json'
    '../results/APPS_qwen2.5-coder_instruction.json'
)

for result_path in "${result_paths[@]}"; do
    echo "$result_path" >> "$output_file"
    for num_cluster in "${num_clusters[@]}"; do
        echo "[Num_cluster = $num_cluster]" >> "$output_file"
        echo "python codebert_kmean.py -b APPS -r $result_path -n $num_cluster"
        output=$(python codebert_kmean.py -b APPS -r "$result_path" -n "$num_cluster")
        num_passed=$(echo "$output" | grep -oP 'num_passed:\s*\K\d+')
        num_total=$(echo "$output" | grep -oP 'num_total:\s*\K\d+')
        echo "num_passed: $num_passed" >> "$output_file"
        echo "num_total: $num_total" >> "$output_file"
        echo "===============================================" >> "$output_file"
    done
done