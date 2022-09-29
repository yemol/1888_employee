'''
Author: yemol yemol_yuan@hotmail.com
Date: 2022-09-24 11:49:55
LastEditors: yemol yemol_yuan@hotmail.com
LastEditTime: 2022-09-29 12:32:35
FilePath: /1888_employee/wxcloudrun/models.py
'''

from datetime import datetime

from django.db import models


class Users(models.Model):
    id = models.AutoField
    openId = models.CharField(max_length=64)
    nickName = models.CharField(max_length=256,default="")
    realName = models.CharField(max_length=64)
    phoneNum = models.CharField(max_length=64, null=True)
    isEmployee = models.BooleanField(default=False, null=True)
    isActor = models.BooleanField(default=False, null=True)
    createdAt = models.DateTimeField(default=datetime.now(), ) 
    updatedAt = models.DateTimeField(default=datetime.now(),)  

    def __str__(self):
        return self.title 

    class Meta:
        db_table = 'Users'  # 数据库表名


class Roles(models.Model):
    roleID = models.AutoField
    roleName = models.CharField(max_length=64)

    def __str__(self):
        return self.title 

    class Meta:
        db_table = 'Roles'  # 数据库表名


class Schedule(models.Model):
    id = models.AutoField
    userId = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)
    roleID = models.ForeignKey('Roles', on_delete=models.SET_NULL, null=True)
    isTest = models.BooleanField(default=False)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    createdAt = models.DateTimeField(default=datetime.now(), )
    updatedAt = models.DateTimeField(default=datetime.now(),)   

    def __str__(self):
        return self.title 

    class Meta:
        db_table = 'Schedule'  # 数据库表名