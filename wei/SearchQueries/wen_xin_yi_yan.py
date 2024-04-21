# -*- coding: utf-8 -*-
import requests
import json

Api_Key = 'lWhmHZbtLONxf5h9jFeDhylF'
Secret_Key = 'afcHp22bfwMSpAMP44DUcd0DL67TPfLK'


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + Api_Key + "&client_secret=" + Secret_Key

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def get_syntax_from_wenxinyiyan(text):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "以下是对需要检索的专利的描述，请根据以下内容生成一个或多个专利检索式,例如：TIABC = (视频识别 or 图形化建模 or 多模态融合 or 迁移学习 or CNN or 大模型 or 神经网络 or 深度学习 or U-Net) and (图片 or 照片 or 脸 or 视频 or 嘴 or 眼 or 表情 or 面部特征 or 人脸图像 or 表情标签) and (脸部识别 or 人脸识别 or 表情分析 or 人脸支付)\n" + text
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    result_data = json.loads(response.text).get('result', None)[:-1]
    print(result_data)
    print("=" * 50)
    return result_data


if __name__ == '__main__':
    get_syntax_from_wenxinyiyan('一种基于注意力机制的商品名称短文本分类方法，包含：对商品名称进行预处理，去除非中文字段以及一些特殊字符；通过jieba分词，将预处理后的商品短文本分成若干个词，去除停用词，对得到的词进行短补长切，统一词的长度到事先设定好的词个数；将每个词利用Global Entity Linking算法进行实体消歧与链接，通过链接到百度百科的外部知识库，用其结果对短文本中的词扩充解释，并将实体链接的结果利用Bert进行word embedding编码，得到相应的特征向量；将得到的向量喂入Transformer网络，利用self‑attention机制，挖掘不同词对于税码分类的共享程度，赋予不同词的不同权重，最后通过Softmax对其进行分类，将概率最高的税码类别作为商品名称所属类别。本发明还包括实施上述发明方法的系统。')
