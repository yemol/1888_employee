
from datetime import datetime
import json
import logging
from signal import SIGTERM
import requests
import time

from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse 
from wxcloudrun.models import Users
from wxcloudrun.models import Schedule, Roles
from django.core import serializers

logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def login(request, _):
    c_openid = None

    #需要使用post，才会附加所需要的用户标识等信息
    if request.method == 'POST' or request.method == 'post':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        #获取OpenID，使用post数据的原因是便于本地调试
        if "openid"  in body.keys() :
            c_openid =  body["openid"]
        else: 
            c_openid = request.META["HTTP_X_WX_OPENID"]

        
        #确认用户是否已经存在
        #如果不存在就创建新用户
        cUser = Users.objects.filter(openId = c_openid)
        if not cUser.exists():
            Users.objects.create(openId = c_openid)
        
        #获取当前登陆用户
        cUser = Users.objects.get(openId = c_openid)

        offset = time.timezone
        logger.info(offset)

        tt = time.localtime()
        current_time = time.strftime("%H:%M:%S", tt)
        logger.info(current_time)

        logger.info(cUser.nickName + ' login on ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' and realName is ' + cUser.realName)
        return JsonResponse({'nickName': cUser.nickName, 'realName': cUser.realName, "isEmployee": cUser.isEmployee, "isActor": cUser.isActor})
    else:
        return JsonResponse({'message': "Error"})


def updateNickName(request, _):
    c_openid = None
    c_nickName = None

    #获取昵称，数据来自小程序
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    c_nickName = body["nickName"]

    #获取OpenID，使用post数据的原因是便于本地调试
    if "openid"  in body.keys() :
        c_openid =  body["openid"]
    else: 
        c_openid = request.META["HTTP_X_WX_OPENID"]

    #获取当前登陆用户
    cUser = Users.objects.filter(openId = c_openid)
    cUser.update(nickName = c_nickName)
    return JsonResponse({'message': "updated"})


def regRole(request, _):
    now = datetime.now()
    roleID = None
    isTest = False

    #需要使用post，才会附加所需要的用户标识等信息
    if request.method == 'POST' or request.method == 'post':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        #获取OpenID，使用post数据的原因是便于本地调试
        if "openid"  in body.keys() :
            c_openid =  body["openid"]
        else: 
            c_openid = request.META["HTTP_X_WX_OPENID"]

        #获得演出相关信息
        roleID = body["roleID"]
        isTest = body["isTest"] == 1

        #获取当前登陆用户
        cUser = Users.objects.get(openId = c_openid)
        cRole = Roles.objects.get(id = roleID)

        #对登记者身份进行合法性检查
        if not cUser.isActor:
             return JsonResponse({'message': "只有演员才能登记演出信息。"} , status=200)

        #更新演出信息
        sItem = Schedule.objects.filter(userId = cUser, year = now.year, month = now.month, day = now.day)
        logger.info(cUser.realName + ' 登记今天出演[角色' + str(roleID) + ']跟场状态为[' + str(isTest) + "]")
        if not sItem.exists():
            Schedule.objects.create(userId = cUser, roleID = cRole, isTest = isTest, year = now.year, month = now.month, day = now.day)
            return JsonResponse({'message': "演出信息已经登记。"} , status=200)
        else:
            sItem.update(roleID = cRole, isTest = isTest, )
            return JsonResponse({'message': "演出信息已经更新。"} , status=200)


def getTodaySchedule(request, _):
    now = datetime.now()
    result = []
    
    #根据日期获取今日演员排班列表
    for item in Schedule.objects.filter(year = now.year, month = now.month, day = now.day):
        result.append({"actor":item.userId.realName, "role": item.roleID.roleName, "isTest": item.isTest})
    return JsonResponse(result, status=200, safe=False)


def myAttendance(request, _):
    result = []
    c_openid = None

    if request.method == 'POST' or request.method == 'post':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        #获取OpenID，使用post数据的原因是便于本地调试
        if "openid"  in body.keys() :
            c_openid =  body["openid"]
        else: 
            c_openid = request.META["HTTP_X_WX_OPENID"]
        
        #根据某个演员的最近90天考勤记录
        for item in Schedule.objects.filter(userId__openId = c_openid).order_by('-createdAt')[:90]:
            result.append(str(item.year) + "-" + str(item.month) + "-" + str(item.day))
        return JsonResponse(result, status=200, safe=False)
    else:
        return JsonResponse({'message': "Plese send request in POST method"})