from collections import defaultdict
import heapq

import jieba.posseg

def word_count(word_list):


    # 创建一个字典用来统计每个元素的出现次数
    count_dict = defaultdict(int)
    for row in word_list:
        for elem in row:
            count_dict[elem] += 1

    most_common = heapq.nlargest(15, count_dict.items(), key=lambda x: x[1])

    res = [value for value, count in most_common]
    print(res)
    return res

def word_count_with_stopword(word_list, stop_word):

    # 创建一个字典用来统计每个元素的出现次数
    count_dict = defaultdict(int)
    for row in word_list:
        for item in row:
            if (item not in stop_word):
                count_dict[item] += 1

    most_common = heapq.nlargest(100, count_dict.items(), key=lambda x: x[1])

    res = [value for value, count in most_common]
    pos = ['n', 'nz']
    seg = jieba.posseg.lcut(' '.join(res))
    new_res = []
    for word, p in seg:
        if(p in pos):
            new_res.append(word)
    res = new_res
    return res

def read_topic():
    # 读取数据
    data = []
    res = []
    with open('wei/SearchQueries/datas/topic.txt', 'r', encoding='utf-8') as file:
        for line in file:
            data.append(line.strip())

    for i in range(int(len(data)/4.0)):
        i = i * 4
        r1 = data[i].split(' ')
        r2 = data[i+1].split(' ')
        r3 = data[i+2].split(' ')
        res.append([r1,r2,r3])

    return res


def match_word(word_list, word_topic):
    res = []
    match = []
    for word_topic_item in word_topic:
        weight = 4
        match_num = 0
        for topic_word_list1 in word_topic_item:
            for topic_word in topic_word_list1:

                if (topic_word in word_list):
                    match_num = match_num + weight * 3
                    match.append(topic_word)
                else:
                    for i in word_list:
                        if (i in topic_word or topic_word in i):
                            match_num = match_num + weight
                            match.append(i)
                            break
            weight = weight / 2
        res.append([word_topic_item, match_num/len(word_list), set(match)])

    res.sort(key=lambda x:x[1], reverse=True)
    filter = 0.4
    filter_res = [item for item in res if item[1] > filter]
    if (len(filter_res)<=0):
        res = [res[0]]
    else:
        res = filter_res

    return res





