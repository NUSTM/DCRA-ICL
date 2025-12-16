import os
import random
import json

from datasets import Dataset, DatasetDict
from uniem.finetuner import FineTuner
from utils.tag_map import get_preference_desc, get_preference

MODEL_PATH = "../models/BAAI.bge-large-zh-v1.5"

random.seed(7777)

def process(raw_data):
    preference_list = get_preference()
    preference_desc = get_preference_desc()

    data = []

    for line in raw_data:
        sentence = line["comment"]
        quadList = line["quadList"]
        if quadList == []:
            pos_name, neg_name = [], []
            pos_name.append(preference_list[3])
            neg_name = preference_list[:3]
            for pos in pos_name:
                for neg in neg_name:
                    try:
                        data.append({
                            "text": sentence,
                            "text_pos": pos + "：" + preference_desc[pos],
                            "text_neg": neg + "：" + preference_desc[neg]
                        })
                    except:
                        print(sentence)
                        print(pos)
        else:
            for quad in quadList:
                preference = quad[3]
                pos_name, neg_name = [], []

                pos_name.append(preference)
                for pref in preference_list:
                    if pref not in pos_name:
                        neg_name.append(pref)
                for pos in pos_name:
                    for neg in neg_name:
                        try:
                            data.append({
                                "text": sentence,
                                "text_pos": pos + "：" + preference_desc[pos],
                                "text_neg": neg + "：" + preference_desc[neg]
                            })
                        except:
                            print(sentence)
                            print(pos)
    return data

def load_train_data():
    dataset = {}
    for key in ["train"]:
        train_dataset = []
        with open(f"../dataset/CompQuad_train_dataset.json", 'r', encoding='utf-8') as file:
            for line in file:
                train_dataset.append(json.loads(line))
        random.shuffle(train_dataset)
        dataset[key] = Dataset.from_list(process(train_dataset))

    return DatasetDict(dataset)

if __name__ == "__main__":

    finetuner = FineTuner.from_pretrained(MODEL_PATH, dataset=load_train_data())
    finetuner.run(
        epochs=3,
        output_dir=f"./tmp/",
        batch_size=4,
        shuffle=True
    )
