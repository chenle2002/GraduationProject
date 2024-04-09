# coding:utf-8
import torch
from importlib import import_module
from django.shortcuts import render, HttpResponse
from system import models


# Create your views here.

def login(request):
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')
    if user_name is None:
        return HttpResponse("登陆失败，输入用户名为空")
    user = models.User.objects.filter(user_name=user_name)[0]
    if user is None:
        return HttpResponse("登陆失败，该用户不存在")
    if user.password == password:
        return HttpResponse("登陆成功")
    return HttpResponse("密码不正确")


def insert(request):
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')
    if user_name is None:
        return HttpResponse("输入用户名为空")
    if password is None:
        return HttpResponse("输入密码为空")
    models.User.objects.create(user_name=user_name, password=password,status=1)

    return HttpResponse("新建用户成功")


def update(request):
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')
    phone = request.GET.get('phone')
    obj = models.User.objects.get(user_name=user_name)  # 先查询
    obj.password = password
    obj.phone = phone
    obj.save()  # 将修改保存到数据库

    return HttpResponse("修改用户信息成功")


def delete(request):
    user_name = request.GET.get('user_name')
    if user_name is None:
        return HttpResponse("删除用户，输入用户名为空")
    models.User.objects.filter(user_name=user_name).delete()
    return HttpResponse("删除用户成功")


def logout(request):
    return HttpResponse('退出')


def predict(request):
    text = "本发明公开了一种基于深度学习的动脉瘤分割方法和装置，其中，该方法包括：获取头部扫描CT血管造影CTA图像；将CTA图像输入到预训练的深度学习模型，基于预训练的深度学习模型对CTA图像进行图像分析处理；其中，预训练的深度学习模型是基于全局定位损失和局部分割损失两个损失函数训练得到，基于图像分析处理，使用动脉瘤分割网络输出相应的脑动脉瘤区域识别分割标签图像。本发明使用CTA图像作为输入，利用三维卷积分割网络和全局定位描述子，能够快速精确检测和分割动脉瘤。用于在医学图像处理领域中基于深度学习执行动脉瘤分割的方法。 用途包括但不限于计算机断层扫描血管造影(CTA)图像、磁共振成像(MRA)图像和脑扫描图像。该方法使得能够使用CTA图像作为使用三维卷积划分网络和全局定位描述符的输入，从而快速和准确地检测和分割动脉瘤。该方法涉及获得头部扫描的头部扫描CT血管造影CTA图像。 将所述CTA图像输入预先训练的深度学习模型。 基于所述预训练的深度学习模型对所述CTA图片进行图像分析处理。 所述深度学习训练基于全局定位损失和局部分割损失两个损失函数。 动脉瘤分割网络，用于基于图像分析处理输出所述脑节段的相应脑节段的相应脑分割标签图像。包括用于基于深度学习执行动脉瘤分割的装置的独立权利要求。"
    print("text:" + text)
    # 定义类别映射
    key = {
        0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
        5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
        10: '10', 11: '11'
    }

    # 加载模型和配置
    model_name = 'bert'
    x = import_module('models.' + model_name)
    config = x.Config('PatentData')
    # model = x.Model(config).to(config.device)
    model = x.Model(config).to("cpu")
    model.load_state_dict(torch.load(config.save_path, map_location='cpu'))

    # 构建预测文本
    def build_predict_text(text):
        token = config.tokenizer.tokenize(text)
        token = ['[CLS]'] + token
        seq_len = len(token)
        mask = []
        token_ids = config.tokenizer.convert_tokens_to_ids(token)
        pad_size = config.pad_size
        if pad_size:
            if len(token) < pad_size:
                mask = [1] * len(token_ids) + ([0] * (pad_size - len(token)))
                token_ids += ([0] * (pad_size - len(token)))
            else:
                mask = [1] * pad_size
                token_ids = token_ids[:pad_size]
                seq_len = pad_size
        ids = torch.LongTensor([token_ids])
        seq_len = torch.LongTensor([seq_len])
        mask = torch.LongTensor([mask])
        return ids, seq_len, mask

    # 进行预测
    data = build_predict_text(text)
    with torch.no_grad():
        outputs = model(data)
        num = torch.argmax(outputs)

    print("预测结果：" + key[int(num)])
    return key[int(num)]
