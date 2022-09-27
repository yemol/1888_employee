'''
Author: yemol yemol_yuan@hotmail.com
Date: 2022-09-24 11:49:55
LastEditors: yemol yemol_yuan@hotmail.com
LastEditTime: 2022-09-27 10:59:21
FilePath: /1888_employee/wxcloudrun/models.py
'''

from datetime import datetime

from django.db import models


# Create your models here.
class Counters(models.Model):
    id = models.AutoField
    count = models.IntegerField(max_length=11, default=0)
    createdAt = models.DateTimeField(default=datetime.now(), )
    updatedAt = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Counters'  # 数据库表名


class Users(models.Model):
    id = models.AutoField
    openId = models.CharField(max_length=64)
    nickName = models.CharField(max_length=256)
    realName = models.CharField(max_length=64)
    phoneNum = models.CharField(max_length=64, null=True)
    isEmployee = models.BooleanField(default=False, null=True)
    createdAt = models.DateTimeField(default=datetime.now(), )
    updatedAt = models.DateTimeField(default=datetime.now(),)   

    def __str__(self):
        return self.title 

    class Meta:
        db_table = 'Users'  # 数据库表名