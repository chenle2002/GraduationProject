# coding=utf-8
from .getIpcFromText import IPCClassifier
from .getWordByCos import TextSimilarity
from .getWordFromText import KeywordExtractor
from .buildPatentRetrievalSyntax import PatentRetrievalSyntaxBuilder
import time

from .util import word_count


class Controller:

    def __init__(self):
        self.KeywordExtractor = KeywordExtractor()
        self.TextSimilarity = TextSimilarity()
        self.IPCClassifier = IPCClassifier()
        self.PatentRetrievalSyntaxBuilder = PatentRetrievalSyntaxBuilder()

    def get_ipc_from_text(self, text):
        return self.IPCClassifier.predict_ipc(text)

    def load_other_data(self, excel_file):
        return self.PatentRetrievalSyntaxBuilder.load_other_data(excel_file)

    def load_target_data(self, excel_file):
        return self.PatentRetrievalSyntaxBuilder.load_target_data(excel_file)

    def build_syntax(self, text):
        print('start')
        t1 = time.time()
        keywords, word_sentences = self.KeywordExtractor.extract_keywords(text)
        similar_keywords,wordMap = self.TextSimilarity.find_similar_keywords(keywords,0.7)
        # similar_keywords,wordMap = self.TextSimilarity.find_similar_keywords(keywords, 0.7)
        ipcList = self.IPCClassifier.predict_ipc(text)

        syntax = self.PatentRetrievalSyntaxBuilder.build(word_sentences, wordMap)
        result = {}
        result['keyWords'] = similar_keywords
        # result['ipc'] = ipcList
        result['syntax'] = syntax
        t2 = time.time()
        print(f"代码执行时间：{t2 - t1} 秒")
        return result

    def get_topic_syntax(self, text):
        result = {}
        print('start')
        t1 = time.time()
        keywords, word_sentences = self.KeywordExtractor.extract_keywords(text)
        keyword_not_stop  = self.KeywordExtractor.data_prepos_not_stop(text)
        similar_keywords, wordMap = self.TextSimilarity.find_similar_keywords(keywords, 0.7)
        print(similar_keywords)
        # similar_keywords,wordMap = self.TextSimilarity.find_similar_keywords(keywords, 0.7)
        keyword_not_stop.extend(similar_keywords)
        print(keyword_not_stop)
        keyword_not_stop = [item for item in set(keyword_not_stop)]
        topic_syntax = self.PatentRetrievalSyntaxBuilder.build_topic_syntax(keyword_not_stop)
        print(topic_syntax)
        new_topic_syntax = []
        for i in topic_syntax:
            new_syntax = ''
            list = i.split(' and ')

            list.reverse()
            print(list)
            for item in list:
                new_syntax = new_syntax + item + ' and '
            new_syntax = new_syntax[: -5]
            new_topic_syntax.append(new_syntax)
        topic_syntax = new_topic_syntax

        similar_keywords.extend(keywords)
        similar_keywords = [item for item in set(similar_keywords)]
        result['keywords'] = similar_keywords
        result['topicSyntax'] = topic_syntax


        t2 = time.time()
        print(f"代码执行时间：{t2 - t1} 秒")
        print()
        return result

    def build_syntax_by_target(self):

        targetData = self.PatentRetrievalSyntaxBuilder.targetData
        otherData = self.PatentRetrievalSyntaxBuilder.otherData
        if (len(targetData) > 0 and len(otherData) > 0):
            syntax = '大模型'
            syntax_old = '大模型'
            r = self.PatentRetrievalSyntaxBuilder.evaluate_for_loop(syntax)
            word_list = word_count(r[3])
            f1 = r[2]

            syntax, r = self.PatentRetrievalSyntaxBuilder.rebuild_for_loop(word_list, syntax, f1)
            f1 = r[2]
            word_list = word_count(r[3])
            for n in range(5):

                for i in range(30):
                    syntax, r = self.PatentRetrievalSyntaxBuilder.rebuild_for_loop(word_list, syntax, f1)
                    f1 = r[2]
                    word_list = word_count(r[3])
                    if (len(word_list) <= 0):
                        # print('f2 _list break')
                        break

                    if (syntax_old == syntax):
                        # print('f2 _old break')
                        break

                    syntax_old = syntax

                new_syntax = self.PatentRetrievalSyntaxBuilder.clear_syntax(syntax)
                if (new_syntax == syntax):
                    # print('f1 break')
                    break

                syntax = new_syntax
                r = self.PatentRetrievalSyntaxBuilder.evaluate_for_loop(syntax)

                word_list = word_count(r[3])
                f1 = r[2]

            # syntax = self.PatentRetrievalSyntaxBuilder.clear_syntax(syntax)
            # r = self.PatentRetrievalSyntaxBuilder.evaluate(syntax)
            # print(syntax)
            # print(r)

            syntax = self.PatentRetrievalSyntaxBuilder.get_output_res(syntax)
            # print(syntax)
            not_word = self.PatentRetrievalSyntaxBuilder.get_not_word()

            result = {}
            result['syntax'] = syntax
            result['notWord'] = not_word
            return result
        else:
            return None


    def loop_build_syntax(self, text):
        result = {}
        print('start')
        t1 = time.time()
        keywords, word_sentences = self.KeywordExtractor.extract_keywords(text)
        keyword_not_stop  = self.KeywordExtractor.data_prepos_not_stop(text)
        similar_keywords, wordMap = self.TextSimilarity.find_similar_keywords(keywords, 0.7)
        print(similar_keywords)
        # similar_keywords,wordMap = self.TextSimilarity.find_similar_keywords(keywords, 0.7)
        ipcList = self.IPCClassifier.predict_ipc(text)
        keyword_not_stop.extend(similar_keywords)
        print(keyword_not_stop)
        keyword_not_stop = [item for item in set(keyword_not_stop)]
        topic_syntax = self.PatentRetrievalSyntaxBuilder.build_topic_syntax(keyword_not_stop)
        print(topic_syntax)
        new_topic_syntax = []
        for i in topic_syntax:
            new_syntax = ''
            list = i.split(' and ')

            list.reverse()
            print(list)
            for item in list:
                new_syntax = new_syntax + item + ' and '
            new_syntax = new_syntax[: -5]
            new_topic_syntax.append(new_syntax)
        topic_syntax = new_topic_syntax
        print(topic_syntax)
        print('===================')
        syntax = ''
        targetData = self.PatentRetrievalSyntaxBuilder.targetData
        otherData = self.PatentRetrievalSyntaxBuilder.otherData
        if(len(targetData)>0 and len(otherData)>0):

            syntax, r = self.PatentRetrievalSyntaxBuilder.build_for_loop(word_sentences, wordMap)
            word_list = word_count(r[3])
            f1 = r[2]
            syntax_old = syntax

            syntax, r = self.PatentRetrievalSyntaxBuilder.rebuild_for_loop(list(keywords), syntax, f1)
            f1 = r[2]
            word_list = word_count(r[3])
            reslist = []
            for n in range(5):

                for i in range(30):
                    syntax, r = self.PatentRetrievalSyntaxBuilder.rebuild_for_loop(word_list, syntax, f1)
                    f1 = r[2]
                    word_list = word_count(r[3])
                    if(len(word_list) <= 0):
                        print('f2 _list break')
                        break

                    if(syntax_old == syntax):
                        print('f2 _old break')
                        break

                    syntax_old = syntax

                new_syntax = self.PatentRetrievalSyntaxBuilder.clear_syntax(syntax)
                if(new_syntax == syntax):
                    print('f1 break')
                    break

                syntax = new_syntax
                r = self.PatentRetrievalSyntaxBuilder.evaluate_for_loop(syntax)

                word_list = word_count(r[3])
                f1 = r[2]

            syntax = self.PatentRetrievalSyntaxBuilder.clear_syntax(syntax)
            r = self.PatentRetrievalSyntaxBuilder.evaluate(syntax)
            print(syntax)
            print(r)

            syntax = self.PatentRetrievalSyntaxBuilder.get_output_res(syntax)
            print(syntax)
            not_word = self.PatentRetrievalSyntaxBuilder.get_not_word()

            result['syntax'] = syntax
            result['not_word'] = not_word

            # new_topic_syntax = []
            # for item in topic_syntax:
            #     item = item + ' and ('+syntax+')'
            #     new_topic_syntax.append(item)
            # topic_syntax = new_topic_syntax

        # new_topic_syntax = []
        # for item in topic_syntax:
        #     item = 'TIAB=('+item+')'
        #     if(len(ipcList)>0):
        #         ipc_syntax = ''
        #         for ipc in ipcList:
        #             ipc_syntax = ipc_syntax+ ipc + ' or '
        #         ipc_syntax = ipc_syntax[: -4]
        #         item = item + ' and IPC-LOW = ('+ipc_syntax+')'
        #     new_topic_syntax.append(item)
        # if (len(ipcList) > 0):
        #     topic_syntax = new_topic_syntax

        result['keyWords'] = similar_keywords
        result['ipc'] = ipcList
        result['topic_syntax'] = topic_syntax


        t2 = time.time()
        print(f"代码执行时间：{t2 - t1} 秒")
        print()
        return result


controller = Controller()

def get_ipc_from_text(text, controller = controller):
    return controller.get_ipc_from_text(text)

def get_topic_syntax(text, controller = controller):
    return controller.get_topic_syntax(text)

def get_topic_syntax(text, controller = controller):
    return controller.get_topic_syntax(text)

def load_other_data(excel_file, controller = controller):
    return controller.load_other_data(excel_file)

def load_target_data(excel_file, controller = controller):
    return controller.load_target_data(excel_file)

def build_syntax_by_target(controller = controller):
    return controller.build_syntax_by_target()

# result = controller.loop_build_syntax('本发明实施例公开了一种用于对语音信号进行语义识别的系统及方法，本发明实施例在电信通讯网络中设置基于注意力机制(Attention)的端到端系统(LAS，Listen, Attention, Spell)、BERT模型及基于神经网络构建的语音文本混合子系统，其中，电信通讯网络中的语音信号输入到LAS中进行语音识别后，得到高维声学特征表示及对应的文本信息，将对应的文本信息输入给BERT模型，将高维声学特征表示输入给语音文本混合子系统中；BERT模型对输入的对应的文本信息进行处理得到高维文本特征表示后，输入给语音文本混合子系统；语音文本混合子系统对输入的高维声学特征表示及高维文本特征表示进行分类处理，得到语义识别结果。本发明通过语音和语义两个模态的信息融合，显著提升对语音信号进行语义识别的准确率。')
# print(result)