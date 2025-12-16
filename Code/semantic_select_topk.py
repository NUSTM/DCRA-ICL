import json
import random
import torch

import torch.nn.functional as F

from tqdm import tqdm
from sentence_transformers import SentenceTransformer


random.seed(7777)
model = SentenceTransformer(
    "./models/BAAI.bge-large-zh-v1.5",
    device="cuda:0"
)

def read_txt(path_file):
    data = []
    with open(path_file, "r", encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def get_examples_idx(model, input, db, topk=5):
    embedding_input = model.encode([input] + db, convert_to_tensor=True, normalize_embeddings=True)
    input_embedding = embedding_input[0]
    db_embedding = embedding_input[1:]

    similarities = F.cosine_similarity(
        input_embedding.unsqueeze(0),
        db_embedding
    )

    topk_scores, topk_indices = torch.topk(similarities, topk)
    res = [i.item() for i in topk_indices]
    return res

def process(source_dataset, dataset, out_file, train_dataset, style="valid"):

    pbar = tqdm(total=len(source_dataset))
    for data in source_dataset:
        global model

        item = data
        bge_examples_idx  = get_examples_idx(model, data["comment"], train_dataset, topk=20)

        item["examples_idx_bge"] = bge_examples_idx

        with open(out_file, "a") as file:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")
        pbar.update(1)
    pbar.close()

if __name__ == "__main__":

    with open(f"../dataset/CompQuad_train.json", 'r', encoding='utf-8') as file:
        CompQuad_train = json.load(file)

    train_dataset = []
    for data in CompQuad_train:
        train_dataset.append(data["comment"])

    source_file = f"" 
    out_file = f"" # validation

    dataset = []
    with open(f"../dataset/CompQuad_train_select_category.json", 'r', encoding='utf-8') as file: # validation
        for line in file:
            item = json.loads(line)
            dataset.append(item)


    source_dataset = read_txt(source_file)

    process(source_dataset, dataset, out_file, train_dataset) 
