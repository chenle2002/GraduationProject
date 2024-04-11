from django.http import JsonResponse
import time
from chenle.TextPredictor import predictor_instance


# Django视图函数
def predict_text(request):
    text = "本发明公开了一种基于深度学习的动脉瘤分割方法和装置，其中，该方法包括：获取头部扫描CT血管造影CTA图像"

    # 开始计时
    start_time = time.time()

    result = predictor_instance.predict(text)

    # 结束计时
    end_time = time.time()

    # 计算方法调用所用时间（单位为秒）并保留两位小数
    elapsed_time = str(round(end_time - start_time, 2))

    print({'result': result, 'elapsed_time': elapsed_time + "秒"})

    return JsonResponse({'result': result, 'elapsed_time': elapsed_time + "秒"})
