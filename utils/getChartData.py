from utils.getPublicData import *
from myApp.models import *


def getIndexData():
    averageCity = list(getaverageCity())
    averageCityX = [x[0] for x in averageCity]
    averageCityY = [round(x[1],1) for x in averageCity]
    print(averageCityX,averageCityY)

    salarycategoryList = list(getsalarycategory())
    salarycategoryData = []
    for i in salarycategoryList:
        salarycategoryData.append({
            'name':i[0],
            'value':i[1]
        })

    expSalaryList = list(getexpSalary())
    expSalaryX = [x[0] for x in expSalaryList]
    expSalaryY1 = [round(x[1],1) for x in expSalaryList]
    expSalaryY2 = [round(x[2],1) for x in expSalaryList]

    peoplecategoryList = list(getpeoplecategory())
    peoplecategoryData = []
    for i in peoplecategoryList:
        peoplecategoryData.append({
            'name':i[0],
            'value':i[1]
        })
    print(salarycategoryData,expSalaryX,expSalaryY1,expSalaryY2,peoplecategoryData)


    adddresssumList = list(getaddresssum())
    adddresssumData = []
    for i in adddresssumList:
        adddresssumData.append({
            'name':i[0],
            'value':i[1]
        })
    print(adddresssumData)
    return averageCityX,averageCityY,salarycategoryData,expSalaryX,expSalaryY1,expSalaryY2,peoplecategoryData,adddresssumData

def addHistoryData(userInfo,jobId):
    hisData = History.objects.filter(user=userInfo,jobId=jobId)
    if len(hisData):
        hisData[0].count += 1
        hisData[0].save()
    else:
        History.objects.create(user=userInfo,jobId=jobId)

def getUserHistory(userInfo):
    dataList = list(History.objects.filter(user=userInfo).order_by('-count'))
    jobIdList = []
    for i in dataList:
        jobIdList.append(i.jobId)
    # print(jobIdList)
    jobList = []
    for i in jobIdList:
        x = list(queryhives('select * from jobData where id = %d',[int(i)],'select')[0])
        print(x)
        jobList.append(x)
    # print(jobList)
    return jobList


def changePwd(userInfo,passwordInfo):
    oldPwd = passwordInfo['oldPassword']
    newPwd = passwordInfo['newPassword']
    chkPwd = passwordInfo['chkPassword']

    user = User.objects.get(username=userInfo.username)

    if oldPwd != user.password :return '原密码错误'
    if newPwd != chkPwd:return '请确认您的密码'
    user.password = newPwd
    user.save()
