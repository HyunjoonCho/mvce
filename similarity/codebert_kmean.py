import json, argparse
import torch
import random
import torch.nn.functional as F
from tqdm import tqdm
from transformers import RobertaTokenizer, RobertaModel
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

model_name = "microsoft/codebert-base"
tokenizer = RobertaTokenizer.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = RobertaModel.from_pretrained(model_name).to(device)
model.eval()

def generating_embedding(results, benchmark):
    embedding_dict = {}

    print("Generating embeddings...")
    for prob, answers in tqdm(results.items()):
        embedding_dict[prob] = []

        for a in answers:
            answer_body = '\n'.join(
                [
                    line for line in a[0].split('\n')
                    if not line.startswith('```') and not line.strip().startswith('def')
                ]
            )

            tokens = tokenizer(
                answer_body,
                return_tensors = 'pt',
                max_length = 512,
                truncation = True,
                padding = 'max_length'
            ).to(device)

            with torch.no_grad():
                outputs = model(**tokens)
                last_hidden_state = outputs.last_hidden_state

                cls_embedding =  last_hidden_state[:, 0, :]
                cls_embedding =  cls_embedding.squeeze(0).cpu()
                embedding_dict[prob].append(cls_embedding)
        
    
    return embedding_dict

def visualize_clusters(clusters, prob):
    embeddings = clusters["embeddings"]
    labels = clusters["labels"]
    centers = clusters["centers"]

    pca = PCA(n_components=2)
    all_points = np.vstack([embeddings, centers])
    all_points_2d = pca.fit_transform(all_points)
    embeddings_2d = all_points_2d[:len(embeddings)]
    centers_2d = all_points_2d[len(embeddings):]

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=labels, cmap='tab10', alpha=0.7, s=50)
    plt.scatter(centers_2d[:, 0], centers_2d[:, 1], c='black', s=100, alpha=0.3, marker='X', label='Cluster Centers')

    plt.title(f'Cluster Visualization for Problem: {prob}')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend()
    plt.grid(True)
    # plt.show()
    plt.savefig(f'./figures/clustering_{prob.replace("/", "_")}')

def kmean_cluster_embeddings(embedding_dict, n_clusters = 5):
    cluster_dict = {}

    for prob, embeddings in embedding_dict.items():
        embedding_np = np.stack([emb.numpy() for emb in embeddings])

        kmeans = KMeans(n_clusters=min(n_clusters, len(embeddings)), random_state=42, n_init='auto')
        labels = kmeans.fit_predict(embedding_np)
        centers = kmeans.cluster_centers_

        cluster_dict[prob] = {
            'embeddings': embedding_np,
            'labels': labels,
            'centers': centers,
            'kmeans': kmeans
        }
    
    return cluster_dict

def get_representative_indices(cluster_dict):
    representative_index_dict = {}

    for prob, data in cluster_dict.items():
        labels = data['labels']
        centers = data["centers"]
        embeddings = data["embeddings"]

        unique, counts = np.unique(labels, return_counts = True)
        largest_cluster_label = unique[np.argmax(counts)]

        cluster_embeddings = embeddings[labels == largest_cluster_label]
        center = centers[largest_cluster_label]

        dists = np.linalg.norm(cluster_embeddings - center, axis = 1)
        closest_idx_with_center = np.argmin(dists)

        global_indices = np.where(labels == largest_cluster_label)[0]
        representative_index_dict[prob] = global_indices[closest_idx_with_center]

    return representative_index_dict


def get_final_answer(results_path, benchmark, num_cluster):
    with open(results_path, 'r') as f:
        results = json.load(f)
    
    final_answer_dict = {}

    # results = {'HumanEval/0': results['HumanEval/0']}
    embedding_dict = generating_embedding(results, benchmark)
    cluster_dict = kmean_cluster_embeddings(embedding_dict, num_cluster)
    # visualize_clusters(cluster_dict['HumanEval/0'], 'HumanEval/0')
    representative_index_dict = get_representative_indices(cluster_dict)

    for prob, index in representative_index_dict.items():
        final_answer = results[prob][index]
        final_answer_body = '\n'.join(
                                [
                                    line for line in final_answer[0].split('\n')
                                    if not line.startswith('```') and not line.strip().startswith('def')
                                ]
                            )
        final_answer_result = final_answer[1]["result"]
        final_answer_dict[prob] = {'body': final_answer_body, 'result': final_answer_result}

    return final_answer_dict


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
    parser.add_argument('-r', '--responses_path', default='../results/HumanEval_llama3.json')
    parser.add_argument('-n', '--num_cluster', default=5)
    args = parser.parse_args()
    assert args.benchmark in['HumanEval', 'APPS']

    final_answer_dict = get_final_answer(args.responses_path, args.benchmark, int(args.num_cluster))
    num_passed, num_total = evaluate(final_answer_dict)
    print(f"num_passed: {num_passed}")
    print(f"num_total: {num_total}")

    result_file = args.responses_path.split('/')[-1]
    result_path = f"./codebert_kmean/{result_file}"

    with open(result_path, 'w') as f:
        json.dump(final_answer_dict, f, indent = 4)
