<!-- 
`category_train.py` 实现了 bge 向量模型的微调。使用category的描述构建正负样本，通过对比学习将category一致的样本，在向量空间中拉近。
`category_select_topk.py` 实现了category-aligned topk个示例的选取。通过微调的 bge 向量模型向量化文本，使用余弦相似度度量样本相似性，选取前k个样本。
`semantic_selct_topk.py` 实现了语义相似的topk个示例的选取。通过 bge 向量模型向量化文本，使用余弦相似度度量样本相似性，选取前k个样本。
`inference.py` 实现了基于双通道检索结果的多种模型的推理。
-->

* `category_train.py`
Implements fine-tuning of the BGE embedding model. It constructs positive and negative samples based on category descriptions and uses contrastive learning to pull samples with the same category closer in the embedding space.

* `category_select_topk.py`
Selects the top-k category-aligned examples. It vectorizes the input texts using the fine-tuned BGE model and measures similarity using cosine similarity, selecting the top-k most similar examples.

* `semantic_selct_topk.py`
Selects the top-k semantic-similar examples. It vectorizes the input texts using the (pretrained) BGE embedding model and uses cosine similarity to identify the top-k closest examples based on semantic similarity.

* `inference.py`
Performs inference using multiple models based on dual-channel retrieval demonstrations.
