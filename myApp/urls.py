from django.contrib import admin
from django.urls import path,include
from myApp import views
import myApp
urlpatterns = [
    path("home/",views.home,name='home'),
    path("login/", views.login, name='login'),
    path("logOut/", views.logOut, name='logOut'),
    path("registry/", views.registry, name='registry'),
    path("salaryChar/", views.salaryChar, name='salaryChar'),
    path("educationChar/", views.educationChar, name='educationChar'),
    path("industryChar/", views.industryChar, name='industryChar'),
    path("cityChar/", views.cityChar, name='cityChar'),
    path("tableData/", views.tableData, name='tableData'),
    path("changeInfo/", views.changeInfo, name='changeInfo'),
    path("collectData/", views.collectData, name='collectData'),
    path("titleCloud/", views.titleCloud, name='titleCloud'),
    path("tagCloud/", views.tagCloud, name='tagCloud'),
    path("recommendPage/", views.recommendPage, name='recommendPage'),
    path("predict/", views.predict, name='predict'),
    # path("collectData/", views.collectData, name='collectData'),
    path("addHistory/<int:jobId>/", views.addHistory, name='addHistory'),
    path("delHistory/<int:jobId>/", views.delHistory, name='delHistory'),
]
