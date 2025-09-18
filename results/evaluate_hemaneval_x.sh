RESULTS_DIR="/workspace/results"
SCRIPT_PATH="/workspace/CodeGeeX/scripts/evaluate_humaneval_x.sh"
N_WORKERS=10

MODELS=("gemini-2.5-flash-lite")
LANGUAGES=("python" "js" "java" "cpp" "go")

echo "Starting HumanEval-X evaluation for all languages..."

for MODEL in "${MODELS[@]}"; do
    for LANG in "${LANGUAGES[@]}"; do
        echo "Evaluating ${LANG}..."
        
        RESULT_FILE="${RESULTS_DIR}/HumanEval-X_${MODEL}_base_${LANG}.jsonl"
        
        if [ ! -f "$RESULT_FILE" ]; then
            echo "Warning: Result file not found: $RESULT_FILE"
            continue
        fi
        
        bash $SCRIPT_PATH $RESULT_FILE $LANG $N_WORKERS
        
        echo "Completed evaluation for ${LANG}"
        echo "----------------------------------------"
    done
done

echo "All evaluations completed!"
