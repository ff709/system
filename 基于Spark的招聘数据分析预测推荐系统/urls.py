"""
URL configuration for 基于Spark的招聘数据分析预测推荐系统 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
#路由文件夹，配置后端接口，渲染数据及网页
from django.contrib import admin
from django.urls import path,include
from myApp import views
import myApp
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",myApp.views.login,name='login'),
    path("myApp/",include('myApp.urls')),
]
