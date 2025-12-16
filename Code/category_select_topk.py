import copy
import json
import random
import torch
import time

import torch.nn.functional as F

from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from utils.tag_map import get_category, get_entity_desc, get_attribute_desc


random.seed(7777)
model = SentenceTransformer(
    "./tmp_category/model",
    device="cuda:0"
)

def read_txt(path_file):
    data = []
    with open(path_file, "r", encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data
  
def get_topk(model, input, keys, topk=5, threshold=0.0):
    embedding = model.encode([input] + keys, convert_to_tensor=True, normalize_embeddings=True)
    input_embedding = embedding[0]
    keys_embedding = embedding[1:]
    similarities = F.cosine_similarity(
        input_embedding.unsqueeze(0),
        keys_embedding
    )
    topk_scores, topk_indices = torch.topk(similarities, topk)
    return [keys[topk_indices[i]] for i in range(len(topk_indices)) if topk_scores[i] >= threshold], [x for x in
                                                                                                      topk_scores if
                                                                                                      x >= threshold]

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

def process(dataset, out_file, train_dataset):
    # global pos, neg
    #
    # entity_list, attribute_list = get_category()
    # entity_desc = get_entity_desc()
    # attribute_desc = get_attribute_desc()
    #
    # category_desc = []
    # for entity in entity_list:
    #     for attribute in attribute_list:
    #         str = entity + "#" + attribute + "：" + entity_desc[entity] + "#" + attribute_desc[attribute]
    #         category_desc.append(str)

    train_data = []
    for data in train_dataset:
        train_data.append(data["comment"])

    boundary = int(len(train_dataset) / 2)

    index_list = []

    pbar = tqdm(total=len(dataset))

    for idx, data in enumerate(dataset):
        global model

        if data["index"] in index_list:
            pbar.update(1)
            continue


        item = copy.deepcopy(data)

        comp_examples_idx  = get_examples_idx(model, data["comment"], train_data[:boundary], topk=20)

        not_examples_idx  = get_examples_idx(model, data["comment"], train_data[boundary:], topk=20)

        not_examples_idx = [x + boundary for x in not_examples_idx]

        item["examples_idx_comp"] = comp_examples_idx 
        item["examples_idx_not"] = not_examples_idx


        with open(out_file, "a") as file:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")
        pbar.update(1)

    pbar.close()

def process_mix(dataset, origin_dataset, out_file, train_dataset):
    global pos, neg

    entity_list, attribute_list = get_category()
    entity_desc = get_entity_desc()
    attribute_desc = get_attribute_desc()

    category_desc = []
    for entity in entity_list:
        for attribute in attribute_list:
            str = entity + "#" + attribute + "：" + entity_desc[entity] + "#" + attribute_desc[attribute]
            category_desc.append(str)

    comp_data = []
    comp_index = []
    not_data = []
    not_index = []
    train_data = []
    for data in train_dataset:
        train_data.append(data["comment"])


    out_dataset = read_txt(out_file)

    index_list = []
    pbar = tqdm(total=len(dataset))

    for index, data in enumerate(dataset):
        global model

        if data["index"] in index_list:
            pbar.update(1)
            continue

        query, score = get_topk(model, data["comment"], category_desc, topk=10, threshold=0.8)
        category = [x.split("：")[0] for x in query]

        item = data

        # 设定一，zero-shot，直接告诉LLM可能的category
        item["category_match"] = category # 或者 item["prompt"] = "这里是包括category的prompt"

        # 设定二，few-shot，根据检索的category选取examples（比较+非比较）
        examples_idx = get_examples_idx(model, data["comment"], train_data, topk=15)

        # comp_examples_idx  = get_examples_idx(model, data["comment"], comp_data, topk=10)

        # not_examples_idx  = get_examples_idx(model, data["comment"], not_data, topk=10)

        # item["examples_idx_comp"] = [comp_index[idx] for idx in comp_examples_idx] # 或者 item["prompt"] = "这里是包括examples的prompt"
        # item["examples_idx_not"] = [not_index[idx] for idx in not_examples_idx]

        if index in examples_idx:
           examples_idx.remove(index)

        item["examples_idx"] = examples_idx

        with open(out_file, "a") as file:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")
        pbar.update(1)
    pbar.close()

if __name__ == "__main__":

    train_dataset = read_txt("../dataset/CompQuad_train_dataset.json")

    source_file = f"../dataset/test_dataset.json"  #
    out_file = f""  

    source_dataset = read_txt(source_file)

    process(source_dataset, out_file, train_dataset) 

    # process_mix(source_dataset, origin_dataset, out_file, train_dataset)
