# coding=utf-8
import random

import jieba
import pandas as pd
import time

from .util import read_topic, match_word, word_count, word_count_with_stopword


class PatentRetrievalSyntaxBuilder:
    def __init__(self, userdict_path='wei/SearchQueries/datas/keyWord.txt', stopwords_path='wei/SearchQueries/datas/stopWord.txt', key_words_path='wei/SearchQueries/datas/keyWord.txt'):
        # 加载停用词
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            self.stopkey = set(word.lower() for word in f.read().splitlines())
        with open(key_words_path, 'r', encoding='utf-8') as f:
            self.key_words = [line.strip() for line in f.read().splitlines()]
        # 加载自定义词库
        jieba.load_userdict(userdict_path)
        self.targetData = []
        self.otherData = []
        # self.targetData = self.getTargetData()
        # self.otherData = self.getOtherData(self.targetData)
        #
        # self.targetTextWord = [set(word.lower() for word in jieba.lcut(text[0] + text[1]) if word not in self.stopkey) for text in self.targetData]
        # self.otherTextWord = [set(word.lower() for word in jieba.lcut(text[0] + text[1]) if word  not in self.stopkey) for text in self.otherData]

    def load_target_data(self, excel_file):
        name = ['标题 (中文)','摘要 (中文)','公开（公告）号']
        df = pd.read_excel(excel_file)
        # 获取列名
        column_names = df.columns
        column_id = {}
        for i in range(len(column_names)):
            if(column_names[i] in name):
                column_id[column_names[i]] = i

        data = df.dropna(subset=[df.columns[i] for i in column_id.values()])
        ti = data.iloc[:, column_id['标题 (中文)']].values
        ab = data.iloc[:, column_id['摘要 (中文)']].values
        id = data.iloc[:, column_id['公开（公告）号']].values

        res = [[ti[i].replace(' ', '').lower(), ab[i].replace(' ', '').lower(), id[i]] for i in range(len(ti))]
        self.targetData = res
        self.targetTextWord = [set(word.lower() for word in jieba.lcut(text[0] + text[1]) if word not in self.stopkey)
                               for text in self.targetData]
        return True

    def load_other_data(self, excel_file):
        name = ['标题 (中文)','摘要 (中文)','公开（公告）号']
        df = pd.read_excel(excel_file)
        # 获取列名
        column_names = df.columns
        column_id = {}
        for i in range(len(column_names)):
            if(column_names[i] in name):
                column_id[column_names[i]] = i

        data = df.dropna(subset=[df.columns[i] for i in column_id.values()])
        ti = data.iloc[:, column_id['标题 (中文)']].values
        ab = data.iloc[:, column_id['摘要 (中文)']].values
        id = data.iloc[:, column_id['公开（公告）号']].values

        res = [[ti[i].replace(' ', '').lower(), ab[i].replace(' ', '').lower(), id[i]] for i in range(len(ti))]
        self.otherData = res
        self.otherTextWord = [set(word.lower() for word in jieba.lcut(text[0] + text[1]) if word not in self.stopkey)
                              for text in self.otherData]
        return True

    def rebuild_for_loop(self, word_list, base_syntax, base_f1):
        t1 = time.time()
        print('start')
        andRelation = self.build_and_relation_for_word_list(word_list)
        res = self.evaluate_list(andRelation)
        res.sort(key=lambda x: x[3], reverse=True)
        res.sort(key = lambda x: len(x[0]), reverse=True)
        syntax_res = self.build_syntax(res, base_syntax, base_f1)
        print(syntax_res)
        r = self.evaluate_for_loop(syntax_res)
        print(r)
        t2 = time.time()
        print(f"代码执行时间：{t2 - t1} 秒")
        return [syntax_res, r]


    def build_for_loop(self, word_sentences, wordMap):
        t1 = time.time()
        print('start')
        andRelation = self.buildAndRelation(word_sentences, wordMap)
        res = self.evaluate_list(andRelation)
        res.sort(key=lambda x: x[3], reverse=True)
        print(len(res))
        print(res)
        # res = res[:10]

        syntax_res = self.build_syntax(res)

        print(syntax_res)
        r = self.evaluate_for_loop(syntax_res)
        print(r)
        t2 = time.time()
        print(f"代码执行时间：{t2 - t1} 秒")
        return [syntax_res, r]

    def build_syntax(self, res , syntax_res = '', f1_res = 0):
        not_used_syntax = []
        not_used_num = 0
        for syntax, recall, precision, f1 in res:
            if (len(syntax_res) <= 0):
                syntax_res = syntax
                f1_res = f1
            else:
                s = syntax_res + ' or ' + syntax
                evaluate_recall, evaluate_precision, evaluate_f1 = self.evaluate(s)
                if (evaluate_f1 > f1_res):
                    syntax_res = s
                    f1_res = evaluate_f1
                else:
                    not_used_syntax.append([syntax, recall, precision, f1])
                    not_used_num = not_used_num + 1
        while (len(not_used_syntax) > 0):
            new_not_used_syntax = []
            new_not_used_num = 0
            for syntax, recall, precision, f1 in not_used_syntax:
                if (len(res) <= 0):
                    syntax_res = syntax
                    f1_res = f1
                else:
                    s = syntax_res + ' or ' + syntax
                    evaluate_recall, evaluate_precision, evaluate_f1 = self.evaluate(s)
                    if (evaluate_f1 > f1_res):
                        syntax_res = s
                        f1_res = evaluate_f1
                    else:
                        new_not_used_syntax.append([syntax, recall, precision, f1])
                        new_not_used_num = new_not_used_num + 1
            if (not_used_num == new_not_used_num):
                break
            else:
                not_used_syntax = new_not_used_syntax
                not_used_num = new_not_used_num
        return syntax_res

    def build(self, word_sentences, wordMap):
        t1 = time.time()
        print('start')
        andRelation = self.buildAndRelation(word_sentences, wordMap)
        res = self.evaluate_list(andRelation)
        res.sort(key=lambda x: x[3], reverse=True)
        print(len(res))
        print(res)
        # res = res[:10]

        syntax_res = self.build_syntax(res)

        print(syntax_res)
        r = self.evaluate(syntax_res)
        print(r)
        t2 = time.time()
        print(f"代码执行时间：{t2 - t1} 秒")
        return [syntax_res, r]

    def build_and_relation_for_word_list(self, word_list):
        res = []

        for i in range(len(word_list)):
            for n in range(i+1,len(word_list)):
                res.append(word_list[i]+' and '+word_list[n])
                # for j in range(n+1,len(word_list)):
                #     res.append(word_list[i] + ' and ' + word_list[n]+' and '+word_list[j])
        res.extend(word_list)
        return res

    def buildAndRelation(self, word_sentences, wordMap):
        res = []
        for sentenceIndex, wordList in word_sentences.items():
            andRelationList = []

            for wordKey in wordList:
                if(wordKey in wordMap):
                    mapWordList = wordMap[wordKey]
                    newList = []
                    for word in mapWordList:
                        for oriWord in andRelationList:
                            newList.append(oriWord+' and '+ word)
                        newList.append(word)
                    andRelationList.extend(newList)
                else:
                    res.append(wordKey)
            res.extend(andRelationList)
        res = set(res)
        print(len(res))
        print(res)
        return res

    def getTargetData(self):
        data = pd.read_excel('./datas/targetData.xlsx').astype(str)
        data = data.dropna(subset=[data.columns[1], data.columns[2], data.columns[3]])
        ti = data.iloc[:, 1].values
        ab = data.iloc[:, 2].values
        id = data.iloc[:, 3].values

        # ipc = data.iloc[:, 15].values

        # all = data.iloc[:, 17].values
        res = [[ti[i].replace(' ', '').lower(),ab[i].replace(' ', '').lower(),id[i]] for i in range(len(ti))]
        return res

    def getOtherData(self, targetData = None):
        data = pd.read_excel('./datas/otherData.xlsx').astype(str)
        data = data.dropna(subset=[data.columns[1], data.columns[2], data.columns[3]])
        ti = data.iloc[:, 1].values
        ab = data.iloc[:, 2].values
        # ipc = data.iloc[:, 15].values
        id = data.iloc[:, 3].values
        # res = [[ti[i], ab[i], ipc[i], id[i]] for i in range(len(ti))]
        if (targetData == None):
            res = [[ti[i].replace(' ', '').lower(), ab[i]].replace(' ', '').lower() for i in range(len(ti))]
        else:
            # res = [[ti[i], ab[i]] for i in range(len(ti))]
            targetId = set(row[2] for row in targetData)
            res = [[ti[i].replace(' ', '').lower(), ab[i].replace(' ', '').lower(), id[i]] for i in range(len(ti)) if id[i] not in targetId]
        # print(len(res))
        # print(len(id))
        return res

    def matching(self, syntax, word_list):
        for itemList in syntax:
            item_match = True
            for item in itemList:
                if(item not in word_list):
                    item_match = False
                    break
            if(item_match):
                return True
        return False


    def transformSyntax(self, patentRetrievalSyntax):
        res = []
        or_split = patentRetrievalSyntax.split('or')
        for split_item in or_split:
            item = []
            and_split = split_item.split('and')
            and_split = [item.strip() for item in and_split]
            for i in and_split:
                item.append(i.strip())
            res.append(item)
        return res

    def evaluate_for_loop(self, patentRetrievalSyntax):
        not_matching_target_list = []
        syntax = self.transformSyntax(patentRetrievalSyntax)
        targetRetrievalNum = 0
        for target_word_list in self.targetTextWord:
            if (self.matching(syntax, target_word_list)):
                targetRetrievalNum = targetRetrievalNum + 1
            else:
                not_matching_target_list.append(target_word_list)
        otherRetrievalNum = 0
        for other in self.otherTextWord:
            if (self.matching(syntax, other)):
                otherRetrievalNum = otherRetrievalNum + 1

        recall = targetRetrievalNum / len(self.targetTextWord)

        if (targetRetrievalNum + otherRetrievalNum <= 0):
            precision = 0
        else:
            precision = targetRetrievalNum / (targetRetrievalNum + otherRetrievalNum)

        if (recall + precision <= 0):
            f1 = 0
        else:
            f1 = 3 * recall * precision / (1 * recall + 2 * precision)

        return recall, precision, f1, not_matching_target_list


    def evaluate(self, patentRetrievalSyntax):
        syntax = self.transformSyntax(patentRetrievalSyntax)
        targetRetrievalNum = 0
        for target in self.targetTextWord:
            if(self.matching(syntax, target)):
                targetRetrievalNum = targetRetrievalNum + 1


        otherRetrievalNum = 0
        for other in self.otherTextWord:
            if(self.matching(syntax, other)):
                otherRetrievalNum = otherRetrievalNum + 1

        recall = targetRetrievalNum / len(self.targetTextWord)

        if (targetRetrievalNum + otherRetrievalNum <= 0):
            precision = 0
        else:
            precision = targetRetrievalNum / (targetRetrievalNum + otherRetrievalNum)

        if (recall + precision <= 0):
            f1 = 0
        else:
            f1 = 3 * recall * precision / (1 * recall + 2 * precision)

        return recall, precision, f1

    def evaluate_list(self, patent_retrieval_syntax_list):
        res = []
        for patent_retrieval_syntax in patent_retrieval_syntax_list:
            recall, precision, f1 = self.evaluate(patent_retrieval_syntax)
            if(f1 > 0.05):
                res.append([patent_retrieval_syntax,recall, precision, f1])
        return res

    def clear_syntax(self, syntax):

        recall, precision, f1 = self.evaluate(syntax)

        item_list = syntax.split(' or ')
        item_list = list(reversed(item_list))
        for item in item_list:
            new_syntax = syntax.replace(' or '+item, '')
            new_recall, new_precision, new_f1 = self.evaluate(new_syntax)
            if(new_f1 > f1):
                syntax = new_syntax
                f1 = new_f1
        return syntax

    def get_output_res(self, syntax):
        print(1111111111111111)
        print(syntax)
        item_list = syntax.split(' or ')
        res = ''
        for i in range(len(item_list)):
            if('and' in item_list[i]):
                res = res + '('+item_list[i]+')'
                res = res + ' or '
            else:
                res = res + item_list[i] + ' or '
        print(res[: -4])
        return res[: -4]

    def build_topic_syntax(self, word_list):
        word_topic = read_topic()
        match_topic_list = match_word(word_list, word_topic)
        res = []
        for match_topic_item in match_topic_list:
            set = []
            word_topic_item = match_topic_item[0]
            syntax = ''
            for word_topic in word_topic_item:
                syntax = syntax + '('
                for topic_word in word_topic:
                    if (topic_word not in set):

                        if (topic_word in word_list or topic_word == word_topic[0]):
                            syntax = syntax + topic_word
                            set.append(topic_word)
                            syntax = syntax + ' or '
                        else:
                            for w in word_list:
                                if (topic_word in w or w in topic_word):
                                    syntax = syntax + topic_word
                                    set.append(topic_word)
                                    syntax = syntax + ' or '
                                    break
                syntax = syntax[: -4]
                syntax = syntax + ')'
                syntax = syntax + ' and '
            syntax = syntax[: -5]
            res.append(syntax)
        return res

    def get_not_word(self):
        target_set = set()

        for target in self.targetTextWord:
            for word in target:
                target_set.add(word)

        not_word = word_count_with_stopword(self.otherTextWord, target_set)

        return not_word

                # wordMap = {'超算': ['极大值', '高通量'], '多模态': ['多模态', '多模态学习', '多模态文本生成', '模态'], '语义': ['语义表示', '词元', '语义理解', '词元化', '词义消歧', '多词一义性', '一元语法'], '数据源': ['开源数据集', '数据整理', '数据源', '数据点', '数据表示', '数据采集', '数据集'], '数据预处理': ['数据整理', '数据生成过程', '数据预处理'], '知识图谱': ['知识图谱', '知识表征'], '监听': [], '疑问词': [], '特征词': ['词特征', '语义特征', '帧特征', '特征表达', '特征图', '实体特征', '语言特征'], '生成式': ['生成器', '生成式建模', '生成式模型', '生成方法', '生成模型'], '数据转换': ['数据转换'], '语义向量': ['语义向量', '词向量', '句向量', '向量化', '句向量表示', '向量', '文本向量'], '生成器': ['生成器', '生成器网络'], '低维': ['降维'], '向量': ['向量', '向量化', '句向量', '语义向量', '偏移向量', '词向量', '基向量'], '升维后': [], '一超算': [], 'GPU': ['通用GPU'], '响应速度': [], '群组': ['聚类', '聚类集成'], '人工智能': ['人工智能', '人工智能领域', '智能体', '智能机器', '通用人工智能', '通用智能'], '自然语言处理': ['自然语言', '自然语言处理', '自然语言生成', '语言处理'], '计算机视觉': ['计算机图像', '计算机视觉', '计算机视觉技术'], '深度学习': ['深度学习', '深度强化学习', '深度学习方法', '浅层学习', '深度Q学习', '学习的学习', '深度学习模型'], '待处理': []}
# word_sentences = {0: {'超算', '多模态', '语义'}, 2: {'数据源', '数据预处理', '知识图谱'}, 3: {'监听'}, 4: {'特征词', '疑问词', '知识图谱'}, 6: {'生成式', '语义'}, 7: {'语义向量', '数据转换', '低维', '向量', '生成器'}, 8: {'低维', '升维后', '向量'}, 10: {'一超算', '超算', 'GPU'}, 12: {'响应速度'}, 13: {'群组'}, 14: {'人工智能'}, 15: {'自然语言处理', '计算机视觉', '深度学习'}, 16: {'群组'}, 18: {'群组', '待处理'}, 19: {'待处理'}, 21: {'群组'}, 22: {'群组'}, 23: {'群组'}}
#
# a = PatentRetrievalSyntaxBuilder()
# # r = a.build(word_sentences, wordMap)
# # r = a.evaluate('自然语言 or 语言 or 语音')
# arr = ['深度学习', '超算', '多模态', '语义', '深度学习', '深度学习', '数据源', '数据预处理', '知识图谱', '深度学习', '监听', '疑问词', '特征词', '知识图谱', '生成式', '语义', '数据转换', '语义向量', '生成器', '低维', '向量', '低维', '向量', '升维后', '一超算', '超算', 'GPU', '深度学习', '深度学习', '响应速度', '深度学习', '群组', '人工智能', '自然语言处理', '计算机视觉', '深度学习', '群组', '群组', '待处理', '待处理', '群组', '群组', '群组']
#
# r = a.build_and_relation_for_word_list(arr)
# print(r)
