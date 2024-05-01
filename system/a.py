# from django.db import models
#
#
# # Create your models here.
# class Views(models.Model):
#     def predict_text(request):
#         return ""
#
#     def process_excel(request):
#         return ""
#
#     def list(self, request, *args, **kwargs):
#         return ""
#
#     def delete(request):
#         return ""
#
#     def judge_exist(request):
#         return ""
#
#     def download(request):
#         return ""
#     def getinfobyid(request):
#         return ""
#     序号 = models.BigIntegerField(blank=True, null=True)
#     标题_中文_field = models.CharField(db_column='标题 (中文)', max_length=255, blank=True,
#                                        null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
#     标题_英文_field = models.TextField(db_column='标题 (英文)', blank=True,
#                                        null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
#     摘要_中文_field = models.TextField(db_column='摘要 (中文)', blank=True,
#                                        null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
#     摘要_英文_field = models.TextField(db_column='摘要 (英文)', blank=True,
#                                        null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
#     申请人 = models.CharField(max_length=255, blank=True, null=True)
#     公开_公告_号 = models.CharField(db_column='公开（公告）号', max_length=255, blank=True,
#                                     null=True)  # Field renamed to remove unsuitable characters.
#     公开_公告_日 = models.CharField(db_column='公开（公告）日', max_length=255, blank=True,
#                                     null=True)  # Field renamed to remove unsuitable characters.
#     申请号 = models.CharField(max_length=255, blank=True, null=True)
#     申请日 = models.CharField(max_length=255, blank=True, null=True)
#     公开类型 = models.CharField(max_length=255, blank=True, null=True)
#     专利类型 = models.CharField(max_length=255, blank=True, null=True)
#     公开国别 = models.CharField(max_length=255, blank=True, null=True)
#     链接到incopat = models.CharField(max_length=255, blank=True, null=True)
#     dwpi用途 = models.TextField(blank=True, null=True)
#     dwpi优势 = models.TextField(blank=True, null=True)
#     dwpi新颖性 = models.TextField(blank=True, null=True)
#     dwpi详细描述 = models.TextField(blank=True, null=True)
#     摘要_技术摘要 = models.TextField(db_column='摘要+技术摘要', blank=True,
#                                      null=True)  # Field renamed to remove unsuitable characters.
#     预测结果 = models.CharField(max_length=255, blank=True, null=True)
#     id = models.BigAutoField(primary_key=True)
#
#     class Meta:
#         managed = True
#         db_table = 'data'
#
#
# class NodeInfo(models.Model):
#     def predict_text():
#         return ""
#
#     def process_excel(self):
#         return ""
#
#     def list(self):
#         return ""
#
#     def judge_exist(self):
#         return ""
#
#     def download(self):
#         return ""
#     def getinfobyid(self):
#         return ""
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50)
#     info = models.CharField(max_length=512)
#
#     class Meta:
#         managed = True
#         db_table = 'node_info'
