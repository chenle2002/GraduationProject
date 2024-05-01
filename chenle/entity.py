from django.db import models


# Create your models here.
class PatentData(models.Model):
    序号 = models.BigIntegerField(blank=True, null=True)
    标题_中文_field = models.CharField(db_column='标题 (中文)', max_length=255, blank=True,
                                       null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    标题_英文_field = models.TextField(db_column='标题 (英文)', blank=True,
                                       null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    摘要_中文_field = models.TextField(db_column='摘要 (中文)', blank=True,
                                       null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    摘要_英文_field = models.TextField(db_column='摘要 (英文)', blank=True,
                                       null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    申请人 = models.CharField(max_length=255, blank=True, null=True)
    公开_公告_号 = models.CharField(db_column='公开（公告）号', max_length=255, blank=True,
                                    null=True)  # Field renamed to remove unsuitable characters.
    公开_公告_日 = models.CharField(db_column='公开（公告）日', max_length=255, blank=True,
                                    null=True)  # Field renamed to remove unsuitable characters.
    申请号 = models.CharField(max_length=255, blank=True, null=True)
    申请日 = models.CharField(max_length=255, blank=True, null=True)
    公开类型 = models.CharField(max_length=255, blank=True, null=True)
    专利类型 = models.CharField(max_length=255, blank=True, null=True)
    公开国别 = models.CharField(max_length=255, blank=True, null=True)
    链接到incopat = models.CharField(max_length=255, blank=True, null=True)
    dwpi用途 = models.TextField(blank=True, null=True)
    dwpi优势 = models.TextField(blank=True, null=True)
    dwpi新颖性 = models.TextField(blank=True, null=True)
    dwpi详细描述 = models.TextField(blank=True, null=True)
    摘要_技术摘要 = models.TextField(db_column='摘要+技术摘要', blank=True,
                                     null=True)  # Field renamed to remove unsuitable characters.
    预测结果 = models.CharField(max_length=255, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'data'


class NodeInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    info = models.CharField(max_length=512)

    class Meta:
        managed = True
        db_table = 'node_info'
class UserPatent(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=50)
    patent_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user_patent'

class Record(models.Model):
    user_name = models.CharField(max_length=20, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    predict = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'record'