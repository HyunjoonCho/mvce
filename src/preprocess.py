import json
import ast
import os
import argparse
from copy import deepcopy

class Augmentor:
    def __init__(self, benchmark, model):
        self.benchmark = benchmark
        self.model = model
        self.data_path = f"../data/{self.benchmark}.jsonl"
        self.result_path = f"../results/{self.benchmark}_{self.model}.json"
        self.output_dir = f"../preprocessed_results/"

    def augment(self):
        data = dict()
        with open(self.data_path, "r") as f:
            for problem in [json.loads(line) for line in f]:
                if self.benchmark == "HumanEval":
                    data[problem["task_id"]] = problem["prompt"]
                elif self.benchmark == "APPS":
                    data[problem["id"]] = problem["question"]


        with open(self.result_path, "r") as f:
            results = json.load(f)
        for problem_id, samples in results.items():
            for sample in samples:
                response = '\n'.join(
                    [
                        line for line in sample[0].split('\n') 
                        if not line.startswith('```') and not line.strip().startswith('def ')
                    ])
                if self.benchmark == "HumanEval":
                    sample[0] = data[problem_id] + response
                elif self.benchmark == "APPS":
                    sample[0] = response

        with open(os.path.join(self.output_dir, f"augmented/{self.benchmark}_{self.model}_augmented.json"), "w") as f:
            json.dump(results, f, indent=4)
        
        return results

class CommentRemover(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.body = [e for e in node.body if not (isinstance(e, ast.Expr) and isinstance(e.value, ast.Constant))]
        self.generic_visit(node)
        return node

class VariableChecker(ast.NodeTransformer):
    def visit_Name(self, node):
        global var_dict, var_id
        self.generic_visit(node)
        if node.id not in var_dict:
            var_dict[node.id] = var_id
            var_id += 1
        return node

    def visit_arg(self, node):
        global var_dict, var_id
        self.generic_visit(node)
        if node.arg not in var_dict:
            var_dict[node.arg] = var_id
            var_id += 1
        return node

class VariableUnifier(ast.NodeTransformer):
    def visit_Name(self, node):
        global var_dict
        self.generic_visit(node)
        node.id = chr(var_dict[node.id])
        return node

    def visit_arg(self, node):
        global var_dict
        self.generic_visit(node)
        node.arg = chr(var_dict[node.arg])
        return node


class Preprocessor:
    def __init__(self, benchmark, model):
        self.benchmark = benchmark
        self.model = model
        self.data_path = f"../data/{self.benchmark}.jsonl"
        self.aug_path = f"../preprocessed_results/augmented/{self.benchmark}_{self.model}_augmented.json"
        self.output_dir = f"../preprocessed_results/"
        
    def record_result(self, dirname, data):
        with open(os.path.join(self.output_dir, f"{dirname}/{self.benchmark}_{self.model}.json"), "w") as f:
            json.dump(data, f, indent=4)
        return

    def ast_preprocess(self):
        with open(self.aug_path, "r") as f:
            data = json.load(f)
        
        for problem_id, samples in data.items():
            for sample in samples:
                try:
                    root = ast.parse(sample[0])
                    comment_remover = CommentRemover()
                    root = comment_remover.visit(root)
                    reduced_sample = ast.unparse(root)
                except:
                    continue
                sample[0] = reduced_sample
        return data
    
    def variable_unify(self, data):
        global var_dict, var_id

        for problem_id, samples in data.items():
            for sample in samples:
                # print("---------------------sample---------------------------")
                # print(sample[0])
                try:
                    var_dict = dict()
                    var_id = 97 # magic number: ascii code of 'a'
                    root = ast.parse(sample[0])
                    # print(ast.dump(root, indent="   "))
                    variable_checker = VariableChecker()
                    variable_unifier = VariableUnifier()

                    inst_root = deepcopy(root)
                    inst_root = variable_checker.visit(inst_root)
                    inst_root = variable_unifier.visit(inst_root)
                    reduced_sample = ast.unparse(inst_root)
                    # print("---------------------reduced---------------------------")
                    # print(reduced_sample)
                except:
                    continue
                sample[0] = reduced_sample

        return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize project with LLM")
    parser.add_argument("mode", type=str)
    args = parser.parse_args()

    # benchmarks = ["HumanEval", "APPS"]
    benchmarks = ["HumanEval"]
    models = ["llama3.1", "llama3", "mistral-nemo", "qwen2.5-coder"]

    if args.mode == "augment":
        for bm in benchmarks:
            for model in models:
                augmentor = Augmenter(bm, model)
                augmentor.augment()
    
    elif args.mode == "ast-only":
        for bm in benchmarks:
            for model in models:
                preprocessor = Preprocessor(bm, model)
                ast_reduced = preprocessor.ast_preprocess()
                preprocessor.record_result("ast_only", ast_reduced)

    elif args.mode == "var-unif":
        for bm in benchmarks:
            for model in models:
                preprocessor = Preprocessor(bm, model)
                ast_reduced = preprocessor.ast_preprocess()
                var_reduced = preprocessor.variable_unify(ast_reduced)
                preprocessor.record_result("var_unif", var_reduced)