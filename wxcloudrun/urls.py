'''
Author: yemol yemol_yuan@hotmail.com
Date: 2022-09-24 11:49:55
LastEditors: yemol yemol_yuan@hotmail.com
LastEditTime: 2022-10-03 01:08:00
FilePath: /1888_employee/wxcloudrun/urls.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""wxcloudrun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from wxcloudrun import views
from django.conf.urls import url

urlpatterns = (

    # 获取本人的考勤记录
    url(r'^^api/myAttendances(/)?$', views.myAttendances),

    # 只是用来更新用户昵称，没有任何用处
    url(r'^^api/myAttendance(/)?$', views.myAttendance),

    # 只是用来更新用户昵称，没有任何用处
    url(r'^^api/updateNickName(/)?$', views.updateNickName),

    # 用户登陆
    url(r'^^api/login(/)?$', views.login),

    # 演员出演登记
    url(r'^^api/regRole(/)?$', views.regRole),

    
    # 获取今日演出安排
    url(r'^^api/getTodaySchedule(/)?$', views.getTodaySchedule),

    # 获取主页
    url(r'(/)?$', views.index),
)
