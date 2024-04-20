# coding=utf-8
import numpy as np
import jieba.posseg
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
import re

class KeywordExtractor:
    def __init__(self, userdict_path='wei/SearchQueries/datas/keyWord.txt', stopwords_path='wei/SearchQueries/datas/stopWord.txt', key_words_path='wei/SearchQueries/datas/keyWord.txt'):
        # 加载自定义词库
        jieba.load_userdict(userdict_path)
        # 加载停用词
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            self.stopkey = set(f.read().splitlines())
        with open(key_words_path, 'r', encoding='utf-8') as f:
            self.key_words = [line.strip() for line in f.read().splitlines()]

    def dataPrepos(self, text):
        # 使用正则表达式按句子分割
        sentences = re.split(r'[，。；]', text)  # 根据逗号、句号、分号进行分句
        l = []
        word_sentences = {}  # 记录每个词出现在哪些句子中
        pos = ['n', 'nz', 'f', 'm', 'x', 'nr', 'v', 'vd', 'vn', 'a', 'd']  # 定义选取的词性

        # 遍历每个句子
        for index, sentence in enumerate(sentences):
            if sentence.strip():  # 确保句子不为空
                seg = jieba.cut(sentence)  # 分词
                for word in seg:
                    if word not in self.stopkey:  # 去停用词
                        l.append(word)
                        if index in word_sentences:
                            word_sentences[index].add(word)  # 添加句子编号，编号从1开始
                        else:
                            word_sentences[index] = {word}
        print(l)
        print(word_sentences)
        return l, word_sentences

    def data_prepos_not_stop(self, text):
        # 使用正则表达式按句子分割
        sentences = re.split(r'[，。；]', text)  # 根据逗号、句号、分号进行分句
        l = []
        pos = ['n', 'nz', 'f', 'm', 'x', 'nr', 'v', 'vd', 'vn', 'a', 'd']  # 定义选取的词性

        # 遍历每个句子
        for index, sentence in enumerate(sentences):
            if sentence.strip():  # 确保句子不为空
                seg = jieba.cut(sentence)  # 分词
                for word in seg:
                    if word:  # 去停用词
                        l.append(word)
        return l

    def extract_keywords(self, text, topK=30, min_weight=0.0):
        print(text)

        text = text.lower()
        print(text)
        corpus = []
        l, word_sentences = self.dataPrepos(text)
        corpus.append(' '.join(l))
        print(corpus)
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(corpus)
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(X)
        words = vectorizer.get_feature_names_out()
        weights = tfidf.toarray()

        all_keywords = []

        keywords_dict = {words[j]: weights[0][j] for j in range(len(words)) if weights[0][j] >= min_weight}
        sorted_keywords = sorted(keywords_dict.items(), key=lambda x: x[1], reverse=True)[:topK]
        all_keywords.append([keyword for keyword, weight in sorted_keywords])

        return set(all_keywords[0]),word_sentences

# # 使用示例
# userdict_path = "datas/keyWord.txt"
# stopwords_path = "datas/stopWord.txt"
#
#
# extractor = KeywordExtractor()
#
# text = "本申请深度学习涉及一种基于超算的多模态海洋知识语义交互方法与系统深度学习，其中，该方法包括：深度学习获取海洋领域数据源进行数据预处理后构建海洋知识图谱；深度学习监听问题语音数据并转换为文本数据，基于文本数据中的疑问词及特征词查询海洋知识图谱中对应的节点及节点间关系确定其问题分类，基于问题分类查询图数据库中的检索结果并生成回答语音数据；构建生成式内容语义交互模型，将文本数据转换为语义向量后利用图片信息生成器得到低维图片向量，将低维图片向量进行升维后输出结果图片；其中，所述方法的生产环境预先部署于一超算平台基于超算GPU集群搭建。通过本申请实现降低模型深度学习发布成本及训练成本，深度学习提升模型响应速度。深度学习本公开提供了一种群组对话方法和装置，涉及人工智能技术领域，具体为自然语言处理、计算机视觉、深度学习等技术领域。具体实现方案为：获取群组对话中对话主体的对话消息；基于对话消息，确定待加入群组对话中的虚拟主体以及待处理问题；基于虚拟主体和待处理问题，得到虚拟主体的回复信息；在群组对话中加入虚拟主体，并通过虚拟主体在群组对话中发出回复信息。该实施方式提高了群组对话中对话主体的对话体验。"
# keywords = extractor.extract_keywords(text)
# print("关键词：", keywords)
#

# def read_all_txt_files(directory):
#     all_texts = []
#     for filename in os.listdir(directory):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(directory, filename)
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 all_texts.append(file.read())  # 添加文件内容到列表
#     return all_texts
#
#


# # 数据预处理操作：分词，去停用词，词性筛选
# def dataPrepos(text, stopkey, keyword):
#     l = []
#     pos = ['n', 'nz', 'f', 'm', 'x', 'nr', 'v', 'vd', 'vn', 'a', 'd']  # 定义选取的词性
#     seg = jieba.cut(text)  # 分词
#     for i in seg:
#         if i not in stopkey:  # 去停用词
#             l.append(i)
#     return l

#
# def dataPrepos(text, stopkey, keyword):
#     # 使用正则表达式按句子分割
#     sentences = re.split(r'[，。；]', text)  # 根据逗号、句号、分号进行分句
#     l = []
#     word_sentences = {}  # 记录每个词出现在哪些句子中
#     pos = ['n', 'nz', 'f', 'm', 'x', 'nr', 'v', 'vd', 'vn', 'a', 'd']  # 定义选取的词性
#
#     # 遍历每个句子
#     for index, sentence in enumerate(sentences):
#         if sentence.strip():  # 确保句子不为空
#             seg = jieba.cut(sentence)  # 分词
#             for word in seg:
#                 if word not in stopkey:  # 去停用词
#                     l.append(word)
#                     if word in word_sentences:
#                         word_sentences[word].add(index + 1)  # 添加句子编号，编号从1开始
#                     else:
#                         word_sentences[word] = {index + 1}
#     print(l)
#     print(word_sentences)
#     return l, word_sentences
#
# # tf-idf获取文本topK关键词
# def getKeywords_tfidf(texts, stopkey, topK, min_weight, keywordsuorce):
#     l, word_sentences = dataPrepos(text[0], stopkey, keywordsuorce)
#     # 数据预处理
#     corpus = [' '.join(l)]
#
#     # 1、构建词频矩阵，将文本中的词语转换成词频矩阵
#     vectorizer = CountVectorizer()
#     X = vectorizer.fit_transform(corpus)  # 词频矩阵
#
#     # 2、统计每个词的tf-idf权值
#     transformer = TfidfTransformer()
#     tfidf = transformer.fit_transform(X)  # 计算tf-idf矩阵
#
#     # 3、获取词袋模型中的所有关键词
#     words = vectorizer.get_feature_names_out()
#
#     # 4、获取tf-idf矩阵
#     weights = tfidf.toarray()
#
#     # 处理每篇文本，提取关键词
#     all_keywords = []
#     for i in range(len(texts)):
#         # 找到权重大于最低权重的词作为关键词
#         keywords = [words[idx] for idx in range(len(words)) if weights[i][idx] >= min_weight]
#
#         # 如果过滤后关键词数量多于topK，则只保留权重最高的topK个
#         if len(keywords) > topK:
#             keywords_idx = np.argsort(-weights[i])[:topK]  # 权重降序排序，取前topK
#             keywords = [words[idx] for idx in keywords_idx]
#
#         all_keywords.append(keywords)
#
#     return all_keywords,word_sentences
#
#
#


# directory = './datas/keyWordSource'
# text = read_all_txt_files(directory)
#

#
# # 示例文本
# text = ["本发明公开了一种用于储能系统的客户提问的答复方法及其装置，该答复方法包括：获取储能设备相关的文本信息；创建知识图谱和基于ChatGPT的知识库，并基于所述文本信息对所述知识图谱和知识库进行训练；接收用户的提问问题，将所述提问问题分别输入到所述知识库和知识图谱中，并分别进行查询，从而得到查询结果；将所述查询结果划分为储能设备相关语义和非储能设备相关语义；将所述储能设备相关语义输入到联邦语言模型得到自然语言回答，将所述自然语言回答和非储能设备相关语义进行融合，展示融合结果。从而实现了用于储能系统的对话客服的功能。"]
#
#
# jieba.load_userdict("./datas/keyWord.txt")
# # 停用词表文件路径
# stopwords_file = "./datas/stopWord.txt"
#
# # 关键词展示的最低权重
# min_weight = 0
#
# # 取权重最高的30个关键词
# topKeyWord = 30
#
# stopkey = []
# # 读取停用词表
# with open(stopwords_file, 'r', encoding='utf-8') as f:
#     stopkey = set(f.read().splitlines())
#
# with open("./datas/keyWord.txt", 'r', encoding='utf-8') as f:
#     keywordsuorce = set(f.read().splitlines())
#
# # 提取关键词
# keywords, word_sentences = getKeywords_tfidf(text, stopkey, topKeyWord, min_weight, keywordsuorce)
# for keywordlist in keywords:
#     for keyword in keywordlist:
#         print(keyword)


