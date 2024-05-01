import base64
import datetime
import os
import time

import pandas as pd
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from chenle.TextPredictor import predictor_instance
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework import status
from django.http import JsonResponse, HttpResponse

from GraduationProject import settings
from chenle import entity
from chenle.serializers.Patent import PatentSerializer
from rest_framework.pagination import PageNumberPagination

from chenle.serializers.Record import RecordSerializer


# Django视图函数
def predict_text(request):
    if request.GET.get('text') is None:
        text = "本发明公开了一种基于深度学习的动脉瘤分割方法和装置，其中，该方法包括：获取头部扫描CT血管造影CTA图像"
    else:
        text = request.GET.get('text')

    user_name = request.GET.get('user_name')
    # 开始计时
    start_time = time.time()

    result = predictor_instance.predict(text)

    # 结束计时
    end_time = time.time()

    # 计算方法调用所用时间（单位为秒）并保留两位小数
    elapsed_time = str(round(end_time - start_time, 2))

    print({'result': result, 'elapsed_time': elapsed_time + "秒"})

    entity.Record.objects.create(user_name=user_name, text=text, predict=result, create_time=datetime.datetime.now())
    return JsonResponse({'result': result, 'elapsed_time': elapsed_time + "秒"})


@csrf_exempt
def process_excel(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        print("开始执行批量打标签")

        # 获取前端传递的列索引字符串和文件名
        column_indices_str = request.POST['columns']
        user_name = request.POST['user_name']

        column_indices = [int(idx) for idx in column_indices_str.split(',') if idx.isdigit()]
        file_name = excel_file.name

        # 读取Excel文件
        df = pd.read_excel(excel_file)

        # 拼合指定列数据得到新数据列
        new_data = ""
        for idx in column_indices:
            new_data += df.iloc[:, idx].astype(str)

        df['摘要+技术摘要'] = new_data

        # 创建预测结果列
        predictions = []

        # 逐行调用predict方法并将结果添加到predictions列表中
        for index, row in df.iterrows():
            prediction = predictor_instance.predict(row['摘要+技术摘要'])
            predictions.append(prediction)

        # 将预测结果列添加到DataFrame中
        df['预测结果'] = predictions

        print("任务完成")
        # 保存处理后的Excel文件到后端本地
        if not os.path.exists('chenle/excel/'):
            os.makedirs('chenle/excel/')
        df.to_excel('chenle/excel/' + user_name + '_processed_' + file_name, index=False)
        print("文件保存到：" + 'chenle/excel/' + user_name + '_processed_' + file_name)
        # 返回处理后的Excel文件路径
        return HttpResponse('Excel文件处理成功')
    else:
        return HttpResponse('请上传Excel文件')


class PatentView(ViewSetMixin, APIView):
    def list(self, request, *args, **kwargs):
        queryset = entity.PatentData.objects.all()
        serializer_class = PatentSerializer
        # 排序
        queryset = queryset.order_by('序号')
        # 分页
        page = PageNumberPagination()
        list = page.paginate_queryset(queryset, self.request, self)
        # 分页之后的结果执行序列化
        ser = serializer_class(instance=list, many=True)
        data = ser.data
        # print("data",data)
        if not data:
            return JsonResponse({'status': status.HTTP_501_NOT_IMPLEMENTED, 'data': data, 'msg': '数据为空'},
                                status=status.HTTP_501_NOT_IMPLEMENTED)

        # 封装返回数据格式
        data = {
            'list': data,
            'pageSize': settings.REST_FRAMEWORK['PAGE_SIZE'],
            'total': queryset.count()
        }

        return JsonResponse({'status': status.HTTP_200_OK, 'data': data},
                            status=status.HTTP_200_OK)


def delete(request):
    id = request.GET.get('id')
    if id is None:
        return HttpResponse("删除序号为空")
    entity.PatentData.objects.filter(序号=id).delete()
    return HttpResponse("删除成功")


def judge_exist(request):
    file_path = 'chenle/excel/' + request.GET.get('user_name') + '_processed_' + request.GET.get('file_name')
    print(file_path)
    if os.path.exists(file_path):
        return HttpResponse("yes")
    else:
        return HttpResponse("no")


def download(request):
    file_path = 'chenle/excel/' + request.GET.get('user_name') + '_processed_' + request.GET.get('file_name')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
            return response
    else:
        return HttpResponse('文件不存在')


def getinfobyid(request):
    id = request.GET.get('id')
    node_info = entity.NodeInfo.objects.get(id=id)

    # 将查询到的对象和图片数据一起封装成JSON格式
    node_dict = {
        'id': node_info.id,
        'name': node_info.name,
        'info': node_info.info,
    }

    # 返回JSON数据到前端
    return JsonResponse(node_dict)


def collect(request):
    patent_id = request.GET.get('id')
    user_name = request.GET.get('user_name')
    entity.UserPatent.objects.create(user_name=user_name, patent_id=patent_id)
    return HttpResponse('收藏成功！')


def getusercollect(request):
    user_name = request.GET.get('user_name')
    user_patents = entity.UserPatent.objects.filter(user_name=user_name)  # 通过用户名筛选相关的专利记录
    patent_ids = set(user_patent.patent_id for user_patent in user_patents)  # 将专利ID放入集合中

    # 查询包含在user_patent_ids中的所有专利数据
    queryset = entity.PatentData.objects.filter(id__in=patent_ids).order_by('id')

    # 分页
    paginator = Paginator(queryset, settings.REST_FRAMEWORK['PAGE_SIZE'])
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 将分页后的结果序列化
    serializer = PatentSerializer(page_obj, many=True)

    # 构建返回数据格式
    data = {
        'list': serializer.data,
        'pageSize': settings.REST_FRAMEWORK['PAGE_SIZE'],
        'total': queryset.count()
    }

    return JsonResponse({'status': status.HTTP_200_OK, 'data': data}, status=status.HTTP_200_OK)


def getrecord(request):
    user_name = request.GET.get('user_name')
    queryset = entity.Record.objects.filter(user_name=user_name)  # 通过用户名筛选相关的记录

    # 分页
    paginator = Paginator(queryset, settings.REST_FRAMEWORK['PAGE_SIZE'])
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 将分页后的结果序列化
    serializer = RecordSerializer(page_obj, many=True)

    # 构建返回数据格式
    data = {
        'list': serializer.data,
        'pageSize': settings.REST_FRAMEWORK['PAGE_SIZE'],
        'total': queryset.count()
    }

    return JsonResponse({'status': status.HTTP_200_OK, 'data': data}, status=status.HTTP_200_OK)