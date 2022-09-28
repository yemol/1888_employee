
from datetime import datetime
import json
import logging
from signal import SIGTERM
import requests

from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse 
from wxcloudrun.models import Counters, Schedule
from wxcloudrun.models import Users
from wxcloudrun.models import Schedule

logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def login(request, _):
    c_openid = None
    c_appid = None
    c = None

    #需要使用post，才会附加所需要的用户标识等信息
    if request.method == 'POST' or request.method == 'post':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        #获取OpenID，使用post数据的原因是便于本地调试
        if "openid"  in body.keys() :
            c_openid =  body["openid"]
        else: 
            c_openid = request.META["HTTP_X_WX_OPENID"]
        #获取AppID
        if "appid"  in body.keys() :
            c_appid =  body["appid"]
        else: 
            c_appid = request.META["HTTP_X_WX_APPID"]
        #获取昵称，数据来自小程序
        c_nickName = body["nickName"]
        
        #确认用户是否已经存在
        #如果不存在就创建新用户
        cUser = Users.objects.filter(openId = c_openid)
        if not cUser.exists():
            Users.objects.create(openId = c_openid,nickName = c_nickName)
        
        #获取当前登陆用户
        cUser = Users.objects.get(openId = c_openid)

        logger.info(cUser.nickName + ' login on ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' and realName is ' + cUser.realName)
        return JsonResponse({'realName': cUser.realName, "isEmployee": cUser.isEmployee, "isActor": cUser.isActor})
    else:
        return HttpResponse("Error call method.", status=200)



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

        #对登记者身份进行合法性检查
        if not cUser.isActor:
             return JsonResponse({'message': "只有演员才能登记演出信息。"} , status=200)

        #更新演出信息
        sItem = Schedule.objects.filter(userId = cUser.id, year = now.year, month = now.month, day = now.day)
        logger.info(cUser.realName + ' 登记今天出演[角色' + str(roleID) + ']跟场状态为[' + str(isTest) + "]")
        if not sItem.exists():
            Schedule.objects.create(userId = cUser.id, roleID = roleID, isTest = isTest, year = now.year, month = now.month, day = now.day)
            return JsonResponse({'message': "演出信息已经登记。"} , status=200)
        else:
            sItem.update(roleID = roleID, isTest = isTest, )
            return JsonResponse({'message': "演出信息已经更新。"} , status=200)


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp

def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})
