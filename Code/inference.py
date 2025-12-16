import json
import copy
import os
import torch
from tqdm import tqdm
import random
import unicodedata
import re
from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM

random.seed(42)

checkpoint = "/root/models/Qwen.Qwen2.5-14B-Instruct"
# tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True).eval()

def read_txt(path_file):
    data = []
    with open(path_file, "r", encoding='utf-8') as file:
        try:
            for idx, line in enumerate(file):
                data.append(json.loads(line))
        except:
            print(idx)
    return data

def conn_qwen2(messages):
    global model, tokenizer
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512,
        do_sample=False,
        output_scores=True
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    res = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return res


def conn_gpt(messages):
    client = OpenAI(
        api_key="",
        base_url=""
    )
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0,
    )
    message = completion.choices[0].message
    content = unicodedata.normalize('NFKC', message.content)
    return content

def run(train_path, origin_path, save_path, style, num, rerank=False, output_type="list"):
    icl_templates = [
'''你是一个比较观点挖掘专家。给定一个手机和它的评论文本，抽取所有的subject-object-category-preference四元组，不需要任何解释。
subject是给定的手机，object是评论中与subject存在直接对比的其他手机，并且object必须包含具体型号。aspect是评论文本中subject与object对比的属性，例如拍照、处理器等。category是aspect的类别，表示为Entity#Attribute，Entity是列表["PHONE","DISPLAY","PROCESSOR","MEMORY&STORAGE","CAMERA","BATTERY&POWER","COMMUNICATION","COOLING","AUDIO DEVICES","PHYSICAL INTERFACE","ACCESSORY","HARDWARE","OS","APP","SERVICE","BRAND"]的一个，Attribute是列表["GENERAL","PRICE","QUALITY","PERFORMANCE","USABILITY","DESIGN","FEATURES","CONNECTIVITY"]的一个。preference是"更好"、"更差"或者"一样"。
要求将object表示为手机品牌与型号拼接的格式，严格按照subject-object-category-preference的顺序，输出一个嵌套列表（例如，[["subject", "object", "category", "preference"]]）。如果没有四元组，仅输出[]。
为方便你进一步理解任务，以下示例供你参考：
{example}
现在，请你基于以上示例，严格按照任务定义，对以下的输入完成四元组的抽取！
注意，如果抽取到的object手机没有指明具体型号，或者与subject没有明确地对比，或者与subject一样，则不认为是一个有效的object，不能构成一个四元组。
输入：{input}
输出：'''
]

    train = []
    with open(train_path, "r", encoding='utf-8') as file:
        for line in file:
            train.append(json.loads(line))


    with open(origin_path, "r") as file:
        for line in file:
            data = json.loads(line)

            index = data["index"]
            name = data["phone_name"]
            comment = data["comment"]
            quadList = data["quadList"]

            output = quadList

            if index in index_list:
                continue

            input = "这是关于" + name + "的产品评论：" + comment
            examples_str = ""
            if style == "random":
                random_idx = data["random_idx"]
                topk_examples = random_idx[:num]
            elif style == "category":
                example_list = data["examples_idx"]
                topk_examples = example_list[:num]
            elif style == "category-sep":
                examples_idx_comp = data["examples_idx_comp"]
                examples_idx_not = data["examples_idx_not"]
                topk_examples_comp = examples_idx_comp[:num]
                topk_examples_not = examples_idx_not[:num]
                topk_examples = []
                half_num = int(num / 2)
                for i in range(half_num):
                    topk_examples.append(topk_examples_comp[i])
                    topk_examples.append(topk_examples_not[i])
            elif style == "mix":
                example_list = data["examples_idx"]
                examples_idx_bge = data["bge_idx"]
                topk_examples_cate = example_list[:num]
                topk_examples_bge = examples_idx_bge[:num]
                topk_examples = []
                half_num = int(num/2)
                for i in range(half_num):
                    topk_examples.append(topk_examples_cate[i])
                    topk_examples.append(topk_examples_bge[i])


            topk_examples.reverse()
            for i in range(num):
                c = topk_examples[i]
                phone = train[c]["phone_name"]
                comment = train[c]["comment"]
                quadList = train[c]["quadList"]
                # if quadList == []:
                #     quadList = [['', '', '', '']]
                example_output = repr(quadList)# if output_type == "list" else get_nl_output(quadList)
                examples_str += "示例" + str(
                    i + 1) + "：\n输入：这是关于" + phone + "的产品评论：" + comment + "\n输出：" + example_output + "\n"

            prompt = icl_templates[0].format(example=examples_str, input=input)
            messages = [{"role": "user", "content": prompt}]
            res = conn_qwen2(messages)
            # res = conn_gpt(messages)
            print(res)

            res = res.replace("\n    ", "").replace("\n", "")#.replace("\'", "\"")
            result = res.split("解释")
            if len(result) > 1:
                res = result[0]
            result = res.split("输出：")
            if len(result) > 1:
                res = result[-1]
            result = res.split("输出:")
            if len(result) > 1:
                res = result[-1]

            last_index = res.rfind("]")
            if last_index != -1:
                if res[last_index - 1] != "]" and res[last_index - 1] != "[":
                    res = res[: last_index + 1] + "]"
                else:
                    res = res[: last_index + 1]

            try:
                label = eval(res)
                res_json = {}
                res_json["prediction"] = label
                res_json["index"] = index
                res_json["gold"] = output

                with open(save_path, "a") as file:
                    file.write(json.dumps(res_json, ensure_ascii=False) + "\n")
            except:
                res_json = {}
                res_json["prediction"] = res
                res_json["index"] = index
                res_json["gold"] = output
                error_path = save_path[:-5] + "_error" + ".json"
                with open(error_path, "a") as file:
                    file.write(json.dumps(res_json, ensure_ascii=False) + "\n")

if __name__ == '__main__':


    train_path = "../dataset/CompQuad_train_dataset.json"
    file_path = ""
    num = 25

    type = ""
    model_type = "gpt4o"
    save_path = f"" 
    run(train_path, file_path, save_path, style="random", num=num)
