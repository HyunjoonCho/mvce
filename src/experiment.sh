#!/bin/bash

# ollama pull llama3.1
# ollama pull mistral-nemo
# ollama pull qwen2.5-coder

# python experiment.py -m llama3 -b HumanEval -p base -r 10
# python experiment.py -m llama3 -b APPS -p base -r 10
# python experiment.py -m llama3 -b HumanEval-X -p base -r 10
# python experiment.py -m llama3.1 -b HumanEval -p base -r 10
# python experiment.py -m llama3.1 -b APPS -p base -r 10
# python experiment.py -m llama3.1 -b HumanEval-X -p base -r 10
# python experiment.py -m mistral-nemo -b HumanEval -p base -r 10
# python experiment.py -m mistral-nemo -b APPS -p base -r 10
# python experiment.py -m mistral-nemo -b HumanEval-X -p base -r 10
# python experiment.py -m qwen2.5-coder -b HumanEval -p base -r 10
# python experiment.py -m qwen2.5-coder -b APPS -p base -r 10
# python experiment.py -m qwen2.5-coder -b HumanEval-X -p base -r 10
# python experiment.py -m phi4 -b HumanEval -p base -r 10
# python experiment.py -m phi4 -b APPS -p base -r 10
# python experiment.py -m phi4 -b HumanEval-X -p base -r 10
# python experiment.py -m gpt-4o -b HumanEval -p base -r 10
# python experiment.py -m gpt-4o -b APPS -p base -r 10
# python experiment.py -m gpt-4o -b HumanEval-X -p base -r 10
python experiment.py -m models/gemini-2.5-flash-lite -b HumanEval -p base -r 10
python experiment.py -m models/gemini-2.5-flash-lite -b APPS -p base -r 10
python experiment.py -m models/gemini-2.5-flash-lite -b HumanEval-X -p base -r 10
