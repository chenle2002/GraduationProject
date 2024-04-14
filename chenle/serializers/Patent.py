# ！/usr/bin/python3
# -*- coding: utf-8 -*-
from rest_framework import serializers

from chenle import entity


class PatentSerializer(serializers.ModelSerializer):

    class Meta:
        model = entity.PatentData
        fields = '__all__'