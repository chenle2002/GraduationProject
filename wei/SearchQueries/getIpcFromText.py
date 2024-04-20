# coding=utf-8
import torch
from transformers import BertTokenizer, BertForSequenceClassification


class IPCClassifier:
    def __init__(self, model_path='wei/SearchQueries/get_ipc_bert', tokenizer_path='wei/SearchQueries/bert_chinese_L-12_H-768_A-12', ipc_label_path='wei/SearchQueries/datas/ipc_label.txt', ipc_text_path='wei/SearchQueries/datas/ipc_text.txt'):
        # 加载模型和分词器
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

        # 加载IPC分类号与标签的映射
        self.ipc_to_label = {}
        self.label_to_ipc = {}
        with open(ipc_label_path, 'r') as file:
            for line in file:
                ipc, label = line.strip().split()
                self.ipc_to_label[ipc] = int(label)
                self.label_to_ipc[int(label)] = ipc

        self.ipc_to_text = {}
        with open(ipc_text_path, 'r', encoding='utf-8') as file:
            for line in file:
                ipc, text = line.strip().split()
                self.ipc_to_text[ipc] = text

    def predict_ipc(self, text):
        # 编码文本
        inputs = self.tokenizer(text, return_tensors="pt", max_length=128, truncation=True, padding=True)

        # 获取模型输出
        with torch.no_grad():
            outputs = self.model(**inputs)

        # 处理模型输出，获取每个标签的概率
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

        print(probabilities)

        top_probs, top_labels = probabilities.topk(3)

        # 转换概率和标签为列表
        top_probs = top_probs.flatten().tolist()
        top_labels = top_labels.flatten().tolist()

        print(top_probs)
        print(top_labels)
        # 获取前三大概率的IPC分类号
        top_ipc = [self.label_to_ipc[label] for label in top_labels]

        res = []
        for i in range(len(top_ipc)):
            if(top_probs[i] > 0.1):
                res.append({'ipc':top_ipc[i],'text':self.ipc_to_text[top_ipc[i]]})

        return res



# model_path = './fine_tuned_bert'
# tokenizer_path = './bert_chinese_L-12_H-768_A-12'
# ipc_label_path = './datas/ipc_label.txt'



# ipc_classifier = IPCClassifier()
#
# text = "本发明属于语音识别技术领域，公开了一种基于API信息的语音识别方法、装置、设备及存储介质。该方法包括：基于用户指令数据，构建训练数据；基于所述训练数据，训练大语言模型，得到初始语音识别模型；基于API定义信息集合，构建提示语，所述API定义信息集合包括多个API定义信息；基于所述提示语，对所述初始语音识别模型进行微调，得到语音识别模型；基于所述语音识别模型，对目标用户指令进行识别，输出识别结果。通过上述方式，在模型训练和推理使用的提示语中加入了对API的描述，使得模型能够额外学习将用户指令判别为特定API的标准，通过嵌入API信息，模型对于API的识别准确率获得了显著提升。"
# print(ipc_classifier.predict_ipc(text))



# {'probabilities': {'G06F40': 0.3853535056114197, 'G06F16': 0.2712113857269287, 'G06N3': 0.19823859632015228}}
# # 加载模型和分词器
# model = BertForSequenceClassification.from_pretrained('./fine_tuned_bert_allipc')
# tokenizer = BertTokenizer.from_pretrained('./bert_chinese_L-12_H-768_A-12')
#
# # 加载IPC分类号与标签的映射
# ipc_to_label = {}
# label_to_ipc = {}
# with open('./datas/ipc_label.txt', 'r') as file:
#     for line in file:
#         ipc, label = line.strip().split()
#         ipc_to_label[ipc] = int(label)
#         label_to_ipc[int(label)] = ipc
#
#
# def predict_ipc(text):
#     # 编码文本
#     inputs = tokenizer(text, return_tensors="pt", max_length=128, truncation=True, padding=True)
#
#     # 获取模型输出
#     with torch.no_grad():
#         outputs = model(**inputs)
#
#     # 处理模型输出，获取每个标签的概率
#     probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
#
#     print(probabilities)
#
#     top_probs, top_labels = probabilities.topk(3)
#
#     # 转换概率和标签为列表
#     top_probs = top_probs.flatten().tolist()
#     top_labels = top_labels.flatten().tolist()
#
#     print(top_probs)
#     print(top_labels)
#     # 获取前三大概率的IPC分类号
#     top_ipc = [label_to_ipc[label] for label in top_labels]
#
#     # 创建结果字典
#     result = {'probabilities': dict(zip(top_ipc, top_probs))}
#
#     return result
#
#
# # 示例
# text = "本发明提出了一种基于图模型的篇章级别事件因果关系抽取方法。本发明进行数据收集并进行训练集合、测试集合的划分；对训练集合进行事件与事件因果关系人工标注；对数据进行预处理操作得到规范化后的输入数据；将规范化后的输入数据通过BERT语言模型获得事件与句子的语义向量；将事件与句子的语义向量利用层次注意力机制获取包含篇章信息的事件语义向量；基于包含篇章信息的事件语义向量利用图模型计算事件因果关系；利用梯度下降算法进行训练得到可用于预测事件因果关系的模型。本发明的事件因果关系抽取性能更加优良，且也能推广至其他类型实体关系、事件关系抽取任务之中。"
# print(predict_ipc(text))
