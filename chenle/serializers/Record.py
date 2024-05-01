# ！/usr/bin/python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from chenle import entity


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = entity.Record
        fields = '__all__'