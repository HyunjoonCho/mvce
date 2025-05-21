import json, argparse
import ast
from zss import simple_distance, Node
from tqdm import tqdm

COMMUTATIVE_OPS = (ast.Add, ast.Mult, ast.BitOr, ast.BitAnd, ast.BitXor)

class Normalize_ast(ast.NodeTransformer):
    def visit_BinOp(self, node):
        self.generic_visit(node)

        if isinstance(node.op, COMMUTATIVE_OPS):
            left_str = ast.unparse(node.left)
            right_str = ast.unparse(node.right)

            if left_str > right_str:
                node.left, node.right = node.right, node.left
        
        return node
    
    def visit_FunctionDef(self, node):
        node.body = [e for e in node.body if not (isinstance(e, ast.Expr) and isinstance(e.value, ast.Constant))]
        self.generic_visit(node)
        return node

def get_final_answer_dict(results_path, preprocessing):
    with open(results_path, 'r') as f:
        results = json.load(f)

    normalizer = Normalize_ast()
    final_answer_dict = {}

    print("Generating normalized trees... ")
    # results = {'HumanEval/93': results['HumanEval/93']}
    for prob, answers in tqdm(results.items()):
        print(prob)
        final_answer_dict[prob] = {}

        trees = []
        zsses = []
        passed = []
        for a in answers:
            try:
                tree = ast.parse(a[0])
                # print(ast.dump(tree, indent=4))
                # print('-'*50)
                if preprocessing:
                    tree = normalizer.visit(tree)
                    ast.fix_missing_locations(tree)
                zss = ast_to_zss(tree)
                trees.append(tree)
                # print(ast.dump(normalized_tree, indent=4))
                # print(ast.unparse(normalized_tree))
                # print("="*50)
                zsses.append(zss)
                passed.append(a[1]['result'])
            except:
                pass
        
        dist_matrix = [[0]*20 for _ in range(20)]
        for i in range(20):
            dist_matrix[i][i] = 1
        
        # print(dist_matrix)
        # print(simple_distance(zsses[0], zsses[0]))
        for i in range(len(zsses)):
            for j in range(i+1, len(zsses)):
                dist_matrix[i][j] = simple_distance(zsses[i], zsses[j])

        
        avg_dists = []
        for i in range(len(zsses)):
            vertical = [dist_matrix[r][i] for r in range(i)]
            horizontal = dist_matrix[i][i+1:]
            avg_dists.append((sum(vertical)+sum(horizontal)) / max((len(zsses)-1), 1))
        
        if avg_dists:
            min_value = min(avg_dists)
            min_index = avg_dists.index(min_value)
            final_answer_dict[prob]['code'] = ast.unparse(trees[min_index])
            final_answer_dict[prob]['result'] = passed[min_index]
            final_answer_dict[prob]['average_distance'] = min_value
        else:
            final_answer_dict[prob]['code'] = None
            final_answer_dict[prob]['result'] = "failed"
            final_answer_dict[prob]['average_distance'] = None
        


        
    return final_answer_dict

def ast_to_zss(node):
    zss_node = Node(type(node).__name__)
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                child = ast_to_zss(item)
                if child:
                    zss_node.addkid(child)
        elif isinstance(value, ast.AST):
            child = ast_to_zss(value)
            if child:
                zss_node.addkid(child)
    return zss_node

def get_zss_node(tree_dict):
    zss_dict = {}

    for prob, trees in tree_dict.items():
        zss_dict[prob] = []
        for tree in trees:
            zss_dict[prob].append(ast_to_zss(tree))
    return zss_dict

def evaluate(final_answer_dict):
    num_passed = 0
    num_total = len(final_answer_dict.keys())
    for final_answer in final_answer_dict.values():
        if final_answer["result"] == "passed":
            num_passed += 1
    
    return num_passed, num_total
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--benchmark', default='HumanEval', type=str, help='Benchmark name')
    parser.add_argument('-r', '--responses_path', default='../preprocessed_results/ast_only/HumanEval_llama3.json')
    parser.add_argument('-p', '--preprocessing', default=False)
    args = parser.parse_args()
    assert args.benchmark in['HumanEval', 'APPS']

    final_answer_dict = get_final_answer_dict(args.responses_path, args.preprocessing)
    num_passed, num_total = evaluate(final_answer_dict)
    print(f"num_passed: {num_passed}")
    print(f"num_total: {num_total}")

    result_file = args.responses_path.split('/')[-1]
    result_path = f"./ast_edit_dist/{result_file}"

    with open(result_path, 'w') as f:
        json.dump(final_answer_dict, f, indent = 4)

    
