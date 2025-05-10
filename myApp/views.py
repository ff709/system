import random

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from utils.getPublicData import *
from utils.getChartData import *
from utils.queryhive import *
from myApp.models import *
from recommend.goRecommend import *
from predict.goPredict import *
# Create your views here.

def home(request):
    if request.method == 'GET':
        averageCityX,averageCityY,salarycategoryData,expSalaryX,expSalaryY1,expSalaryY2,peoplecategoryData,adddresssumData = getIndexData()
        sorted_arr = list(getsalaryTop())
        return render(request,'home.html',{
            'averageCityX':averageCityX,
            'averageCityY':averageCityY,
            'salarycategoryData':salarycategoryData,
            'expSalaryX':expSalaryX,
            'expSalaryY1':expSalaryY1,
            'expSalaryY2':expSalaryY2,
            'peoplecategoryData':peoplecategoryData,
            'adddresssumData':adddresssumData,
            'sorted_arr':sorted_arr
        })


def logOut(request):
    request.session.clear()
    return redirect('login')

def login(request):
    if request.method == 'GET':
        return render(request,'login.html',{

        })
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        print(uname,pwd)
        try:
            user = User.objects.get(username=uname,password=pwd)
            request.session['username'] = uname
            return redirect('/myApp/home/')
        except:
            messages.error(request,'请输入正确的用户名与密码')
            return HttpResponseRedirect('/myApp/login/')
        return render(request,'login.html',{

        })


def registry(request):
    if request.method == 'GET':
        return render(request,'registry.html',{

        })
    else:
        uname = request.POST.get('username')
        password = request.POST.get('password')
        ckPassword = request.POST.get('ckPassword')
        print(uname,password,ckPassword)
        try:
            User.objects.get(username=uname)
            message = '用户名已注册'
        except:
            if not uname or not password or not ckPassword:
                message = '注册信息不能为空'
                messages.error(request,message)
                return HttpResponseRedirect('/myApp/registry/')
            elif password != ckPassword:
                message = '两次密码不相符，请重新输入'
                messages.error(request, message)
                return HttpResponseRedirect('/myApp/registry/')
            else:
                User.objects.create(username=uname,password=password)
                messages.success(request, '注册成功')
                return HttpResponseRedirect('/myApp/login/')
        return render(request,'registry.html',{

        })




def salaryChar(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        typeSalaryList = list(gettypeSalary())
        print(typeSalaryList)
        typeSalaryX = [x[0] for x in typeSalaryList]
        print(typeSalaryX)
        typeSalaryY1 = list(typeSalaryList[0][1:])
        typeSalaryY2 = list(typeSalaryList[1][1:])
        typeSalaryY3 = list(typeSalaryList[2][1:])
        typeSalaryY4 = list(typeSalaryList[3][1:])
        typeSalaryY5 = list(typeSalaryList[4][1:])
        typeSalaryY6 = list(typeSalaryList[5][1:])
        typeSalaryY7 = list(typeSalaryList[6][1:])
        # print(typeSalaryY7)
        averageTypeList = list(getaverageType())
        averageTypeData = []
        for i in averageTypeList:
            averageTypeData.append({
                'name':i[0],
                'value':float(round(i[1],1))
            })
        print(averageTypeData)
        return render(request,'index.html',{
            'userInfo':userInfo,
            'typeSalaryX':typeSalaryX,
            'typeSalaryY1':typeSalaryY1,
            'typeSalaryY2': typeSalaryY2,
            'typeSalaryY3': typeSalaryY3,
            'typeSalaryY4': typeSalaryY4,
            'typeSalaryY5': typeSalaryY5,
            'typeSalaryY6': typeSalaryY6,
            'typeSalaryY7': typeSalaryY7,
            'averageTypeData':averageTypeData
        })



def educationChar(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)

        averageExperienceList = list(getaverageExperience())
        averageExperienceX = [x[0] for x in averageExperienceList]
        averageExperienceY1 = [round(x[1],1) for x in averageExperienceList]
        averageExperienceY2 = [x[2] for x in averageExperienceList]
        print(averageExperienceX,averageExperienceY1,averageExperienceY2)

        educationCountList = list(geteducationCount())
        educationCountData = []
        for i in educationCountList:
            educationCountData.append({
                'name':i[0],
                'value':i[1],
                'unit': '人'
            })
        print(educationCountData)
        return render(request,'educationChar.html',{
            'userInfo':userInfo,
            'averageExperienceX':averageExperienceX,
            'averageExperienceY1':averageExperienceY1,
            'averageExperienceY2':averageExperienceY2,
            'educationCountData':educationCountData
        })

def industryChar(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)

        typeCountList = list(gettypeCount())
        typeCountX = [x[0] for x in typeCountList]
        typeCountY = [x[1] for x in typeCountList]

        typeMaxList = list(gettypeMax())
        typeMaxData = []
        for i in typeMaxList:
            typeMaxData.append({
                'name':i[0],
                'value':i[1]
            })
        print(typeCountX,typeCountY,typeMaxData)
        return render(request,'industryChar.html',{
            'userInfo':userInfo,
            'typeCountX':typeCountX,
            'typeCountY':typeCountY,
            'typeMaxData':typeMaxData
        })

def cityChar(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)

        citySalaryList = list(getcitySalary())
        cityPeopleList = list(getcityPeople())
        selectList = [x[0] for x in citySalaryList]
        defaultCity = request.GET.get('city') or '广州'
        print(defaultCity)
        print(selectList)
        citySalaryX = ['0-5000','5000-7000','7000-10000','10000-20000','20000以上',]
        citySalaryY = list(queryhives('select * from citySalary where city = %s',[defaultCity],'select')[0])[1:]


        cityPeopleData = list(queryhives('select * from cityPeople where city = %s',[defaultCity],'select')[0])[1:]

        cityPeopleReal = [
            {
                'name':'0-10人',
                'value':cityPeopleData[0]
            },
            {
                'name': '10-50人',
                'value': cityPeopleData[1]
            },
            {
                'name': '50-150人',
                'value': cityPeopleData[2]
            },
            {
                'name': '150-500人',
                'value': cityPeopleData[3]
            },
            {
                'name': '500-100人',
                'value': cityPeopleData[4]
            },
            {
                'name': '1000以上',
                'value': cityPeopleData[5]
            },
        ]
        print(cityPeopleReal,citySalaryX,citySalaryY)
        return render(request,'cityChar.html',{
            'userInfo':userInfo,
            'selectList':selectList,
            'defaultCity':defaultCity,
            'cityPeopleReal':cityPeopleReal,
            'citySalaryX':citySalaryX,
            'citySalaryY':citySalaryY
        })



def tableData(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        tableData = list(getjobData())
        return render(request,'tableData.html',{
            'userInfo':userInfo,
            'tableData':tableData[:20]
        })


def collectData(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        jobList = getUserHistory(userInfo)
        return render(request,'collectData.html',{
            'userInfo':userInfo,
            'jobList':jobList
        })

def titleCloud(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)

        return render(request,'titleCloud.html',{
            'userInfo':userInfo,

        })


def tagCloud(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)

        return render(request,'tagCloud.html',{
            'userInfo':userInfo,

        })


def predict(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        jobDataList = list(getjobData())
        cityList = list(set(x[12] for x in jobDataList))
        expList = list(set(x[5] for x in jobDataList))
        eduList = list(set(x[6] for x in jobDataList))
        return render(request,'predict.html',{
            'userInfo':userInfo,
            'cityList':cityList,
            'expList':expList,
            'eduList':eduList
        })
    else:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        jobDataList = list(getjobData())
        cityList = list(set(x[12] for x in jobDataList))
        expList = list(set(x[5] for x in jobDataList))
        eduList = list(set(x[6] for x in jobDataList))
        defaultCity = request.POST.get('city')
        defaultExp = request.POST.get('workExp')
        defaultEdu = request.POST.get('education')
        print(defaultCity,defaultEdu,defaultExp)
        predicted_salary = pred_salary(defaultCity,defaultExp,defaultEdu)
        return render(request,'predict.html',{
            'userInfo':userInfo,
            'cityList':cityList,
            'expList':expList,
            'eduList':eduList,
            'defaultCity':defaultCity,
            'defaultEdu':defaultEdu,
            'defaultExp':defaultExp,
            'predicted_salary':predicted_salary
        })



def recommendPage(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        dataList = list(History.objects.filter(user=userInfo).order_by('-count'))
        jobIdList = []
        for i in dataList:
            jobIdList.append(i.jobId)
        realJob = queryhives('select title from jobData where id = %d',[int(jobIdList[0])],'select')[0][0]
        print(realJob)
        try:
            recommend_title = get_recommendations(realJob)[:20]
        except:
            recommend_title = get_recommendations('测试工程师[奥运村]')[:20]
        idList = []
        for i in recommend_title:
            idList.append(i[1])
        recommendList = []
        for i in idList:
            x = list(queryhives('select * from jobData where id = %d',[int(i)],'select')[0])
            recommendList.append(x)

        if len(recommendList) > 12:
            recommendList = random.sample(recommendList,12)

        return render(request,'recommenPage.html',{
            'userInfo':userInfo,
            'recommendList':recommendList
        })

def changeInfo(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)

    if request.method == 'POST':
        print(request.POST)
        res = changePwd(userInfo,request.POST)
        if res != None:
            messages.error(request,res)
            return HttpResponseRedirect('/myApp/changeInfo/')
        userInfo = User.objects.get(username=uname)
        messages.success(request,'修改成功')
    return render(request,'changeInfo.html',{
        'userInfo':userInfo,
    })


def addHistory(request,jobId):
    uname = request.session.get('username')
    print(request.session.get('username'))
    a = uname
    userInfo = User.objects.get(username=a)
    print(jobId)
    addHistoryData(userInfo,jobId)

    return HttpResponseRedirect('/myApp/collectData')


def delHistory(request,jobId):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    print(request.session.get('username'))
    data = History.objects.filter(jobId=jobId)
    data.delete()
    return redirect('/myApp/collectData')
