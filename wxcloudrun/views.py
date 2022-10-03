
import datetime
import json
import logging
from signal import SIGTERM
import requests
import time,os

from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse 
from wxcloudrun.models import Users
from wxcloudrun.models import Schedule, Roles, Covids
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

        logger.info(cUser.nickName + ' login on ' + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' and realName is ' + cUser.realName)
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
    # 因为系统问题，我们必须手动增加8小时
    now = datetime.datetime.now() + datetime.timedelta(hours = 8)
    roleID = None
    isTest = False
    startTemperature = None
    endTemperature  = None
    checkedIn24Hours = True

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
        startTemperature = body["startTemperature"]
        endTemperature = body["endTemperature"]
        checkedIn24Hours = body["checkedIn24Hours"] == 1

        #获取当前登陆用户
        cUser = Users.objects.get(openId = c_openid)
        cRole = Roles.objects.get(id = roleID)

        #记录核酸检查相关信息，或许以后就不需要了，所以将逻辑单独分离出来，不和主体进行合并。
        sCovid = Covids.objects.filter(user = cUser, year = now.year, month = now.month, day = now.day)
        if not sCovid.exists():
            Covids.objects.create(
                user = cUser, startTemperature = startTemperature, endTemperature = endTemperature,  checkedIn24Hours = checkedIn24Hours, 
                year = now.year, month = now.month, day = now.day
            )
        else:
            sCovid.update(startTemperature = startTemperature, endTemperature = endTemperature,  checkedIn24Hours = checkedIn24Hours)


        #只有演员需要登记演出信息
        if cUser.isActor:
            #更新演出信息
            sItem = Schedule.objects.filter(userId = cUser, year = now.year, month = now.month, day = now.day)
            logger.info(cUser.realName + ' 登记今天出演[角色' + str(roleID) + ']跟场状态为[' + str(isTest) + "]")
            if not sItem.exists():
                Schedule.objects.create(userId = cUser, roleID = cRole, isTest = isTest, year = now.year, month = now.month, day = now.day)
                return JsonResponse({'message': "信息已经登记。"} , status=200)
            else:
                sItem.update(roleID = cRole, isTest = isTest, )
                return JsonResponse({'message': "信息已经更新。"} , status=200)
        else:
            return JsonResponse({'message': "核酸检测信息登记完成。"} , status=200)




def getTodaySchedule(request, _):
    # 因为系统问题，我们必须手动增加8小时
    now = datetime.datetime.now() + datetime.timedelta(hours = 8)
    result = []
    
    #根据日期获取今日演员排班列表
    for item in Schedule.objects.filter(year = now.year, month = now.month, day = now.day):
        result.append({"actor":item.userId.realName, "role": item.roleID.roleName, "isTest": item.isTest})
    return JsonResponse(result, status=200, safe=False)


def getTodayCovids(request, _):
    # 因为系统问题，我们必须手动增加8小时
    now = datetime.datetime.now() + datetime.timedelta(hours = 8)
    result = []
    
    #根据日期获取今日演员排班列表
    logger.info(now.strftime("%m/%d/%Y, %H:%M:%S") + " 尝试获取当日核酸检查数据")
    for item in Covids.objects.filter(year = now.year, month = now.month, day = now.day):
        result.append({"actor":item.userId.realName, "startTemperature": item.startTemperature, "endTemperature": item.endTemperature, "checkedIn24Hours": item.checkedIn24Hours})
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


def myAttendances(request, _):
    days = []
    roles = []
    tests = []
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
            days.append(str(item.year) + "-" + str(item.month) + "-" + str(item.day))
            roles.append(str(item.roleID.roleName))
            tests.append(str(item.isTest))

        return JsonResponse({
            "days": days, 
            "roles": roles, 
            "tests" : tests
        }, status=200, safe=False)
    else:
        return JsonResponse({'message': "Plese send request in POST method"})