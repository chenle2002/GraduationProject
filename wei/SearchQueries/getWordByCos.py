import pandas as pd
from sentence_transformers import SentenceTransformer
import umap
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class TextSimilarity:
    def __init__(self, model_name='wei/SearchQueries/distiluse-base-multilingual-cased-v1', stop_words_path='wei/SearchQueries/datas/stopWord.txt', key_words_path='wei/SearchQueries/datas/keyWord.txt'):
        # 加载模型
        self.model = SentenceTransformer(model_name)
        # 加载停用词
        with open(stop_words_path, 'r', encoding='utf-8') as f:
            self.stop_words = set(f.read().splitlines())
        # 获取文本数据列
        with open(key_words_path, 'r', encoding='utf-8') as f:
            self.text_data = [line.strip() for line in f.read().splitlines() if line not in self.stop_words]
        # 初始化 UMAP
        # self.umap_reducer = umap.UMAP(n_neighbors=15, n_components=2)
        # 对文本数据进行向量化并降维
        self.vectors = self.model.encode(self.text_data)
        # self.umap_embeddings = self.umap_reducer.fit_transform(vectors)

    def find_similar_keywords(self, input_professions, similarity_threshold=0.7):
        # 对用户输入的专业名词进行向量化
        input_professions = list(input_professions)
        input_vectors = self.model.encode(list(input_professions))
        # 寻找与用户输入的专业名词最相近的专业名词
        closest_profession_indices = []
        index = 0
        wordMap = {}
        for input_vector in input_vectors:
            similarities = cosine_similarity([input_vector], self.vectors)
            closest_indices = np.where(similarities[0] > similarity_threshold)[0]
            if len(closest_indices) > 7:
                closest_indices = closest_indices[np.argsort(similarities[0, closest_indices])[-7:]][::-1]
            closest_profession_indices.extend(closest_indices)
            wordMap[input_professions[index]] = [self.text_data[i] for i in closest_indices if len(self.text_data[i]) > 0]
            print(input_professions[index], len(closest_indices), wordMap[input_professions[index]])
            index = index + 1
        closest_profession_indices = list(set(closest_profession_indices))
        result = [self.text_data[index] for index in closest_profession_indices]
        return result,wordMap



# text_similarity = TextSimilarity()
# input_professions = ['超算', '多模态', '语义', '数据源', '数据预处理', '知识图谱', '监听', '疑问词', '特征词', '知识图谱', '生成式', '语义', '数据转换', '语义向量', '生成器', '低维', '向量', '低维', '向量', '升维后', '一超算', '超算', 'GPU', '响应速度', '群组', '人工智能', '自然语言处理', '计算机视觉', '深度学习', '群组', '群组', '待处理', '待处理', '群组', '群组', '群组']
# similar_keywords,wordMap = text_similarity.find_similar_keywords(input_professions)
# print("与输入专业名词最相近的专业名词为:", similar_keywords)
# print(wordMap)


#
# # 读取停用词表文件
# stop_words_path = './datas/stopWord.txt'
# with open(stop_words_path, 'r', encoding='utf-8') as f:
#     stop_words = set(f.read().splitlines())
#
# # 读取xlsx文件
# data = pd.read_excel('./datas/大模型关键词表.xlsx').astype(str)
#
# # 获取文本数据列
# with open('datas/keyWord.txt', 'r', encoding='utf-8') as f:
#     text_data = [line.strip() for line in f.read().splitlines()]
#
# # 加载 Sentence-BERT 模型
# model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
#
# # 使用 UMAP 进行降维
# umap_reducer = umap.UMAP(n_neighbors=15, n_components=2)
#
# # 输出数据数量
# print(f"数据数量: {len(text_data)}")
#
# # 对文本数据进行向量化
# vectors = model.encode(text_data)
#
# # 使用 UMAP 进行降维
# umap_embeddings = umap_reducer.fit_transform(vectors)
#
#
# input_professions = ['语义', '知识图谱', '知识库', '自然语言', 'chatgpt', '语言模型']
#
#
# # 对用户输入的专业名词进行向量化
# input_vectors = model.encode(input_professions)
#
# umap_vectors = umap_reducer.fit_transform(input_vectors)
#
# # 设置余弦相似度阈值
# similarity_threshold = 0.7
#
# # 寻找与用户输入的专业名词最相近的xlsx文件的专业名词（取前10个）
# closest_profession_indices = []
# index = 0
# for input_vector in input_vectors:
#     # 计算用户输入的专业名词与所有文本数据的余弦相似度
#     similarities = cosine_similarity([input_vectors], vectors)
#
#     # 找到余弦相似度高于阈值的专业名词索引
#     closest_indices = np.where(similarities[0] > similarity_threshold)[0]
#     # 如果找到的专业名词数量超过10个，则取相似度最高的前10个
#     print(input_professions[index],len(closest_indices),[text_data[i] for i in closest_indices])
#     index = index + 1
#     if len(closest_indices) > 7:
#         closest_indices = closest_indices[np.argsort(similarities[0, closest_indices])[-7:]][::-1]
#     closest_profession_indices.extend(closest_indices)
#
# # 去除重复的索引
# closest_profession_indices = list(set(closest_profession_indices))
#
# result = []
# for word in closest_profession_indices:
#     if word not in stop_words:
#         result.append(word)
#
#
# # 输出结果
# print("与输入专业名词最相近的专业名词为:")
# for index in closest_profession_indices:
#     word = text_data[index]
#     if word not in stop_words:
#         result.append(word)
#         print(word)
#
