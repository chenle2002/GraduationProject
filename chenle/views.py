import time

from chenle.TextPredictor import predictor_instance
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework import status
from django.http import JsonResponse, HttpResponse

from GraduationProject import settings
from chenle import entity
from chenle.serializers.Patent import PatentSerializer
from rest_framework.pagination import PageNumberPagination


# Django视图函数
def predict_text(request):
    if request.GET.get('text') is None:
        text = "本发明公开了一种基于深度学习的动脉瘤分割方法和装置，其中，该方法包括：获取头部扫描CT血管造影CTA图像"
    else:
        text = request.GET.get('text')

    # 开始计时
    start_time = time.time()

    result = predictor_instance.predict(text)

    # 结束计时
    end_time = time.time()

    # 计算方法调用所用时间（单位为秒）并保留两位小数
    elapsed_time = str(round(end_time - start_time, 2))

    print({'result': result, 'elapsed_time': elapsed_time + "秒"})

    return JsonResponse({'result': result, 'elapsed_time': elapsed_time + "秒"})


def delete(request):
    id = request.GET.get('id')
    if id is None:
        return HttpResponse("删除序号为空")
    entity.PatentData.objects.filter(序号=id).delete()
    return HttpResponse("删除成功")

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
