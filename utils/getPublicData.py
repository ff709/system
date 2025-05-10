from utils.queryhive import queryhives

def getjobData():
    jobData = queryhives('select * from jobData',[],'select')
    return jobData

def getaverageCity():
    averageCity = queryhives('select * from averageCity',[],'select')
    return averageCity

# print(getaverageCity()[0])
def getsalarycategory():
    salarycategory = queryhives('select * from salarycategory',[],'select')
    return salarycategory


def getexpSalary():
    expSalary = queryhives('select * from expSalary',[],'select')
    return expSalary

def getaddresssum():
    addresssum = queryhives('select * from addresssum',[],'select')
    return addresssum


def getpeoplecategory():
    peoplecategory = queryhives('select * from peoplecategory',[],'select')
    return peoplecategory

def getsalaryTop():
    salaryTop = queryhives('select * from salaryTop',[],'select')
    return salaryTop

def gettypeSalary():
    typeSalary = queryhives('select * from typeSalary',[],'select')
    return typeSalary

def getaverageType():
    averageType = queryhives('select * from averageType',[],'select')
    return averageType

# print(getaverageType()[0])
def getaverageExperience():
    averageExperience = queryhives('select * from averageExperience',[],'select')
    return averageExperience

def geteducationCount():
    educationCount = queryhives('select * from educationCount',[],'select')
    return educationCount


def gettypeCount():
    typeCount = queryhives('select * from typeCount',[],'select')
    return typeCount

def gettypeMax():
    typeMax = queryhives('select * from typeMax',[],'select')
    return typeMax

def getcitySalary():
    citySalary = queryhives('select * from citySalary',[],'select')
    return citySalary

def getcityPeople():
    cityPeople = queryhives('select * from cityPeople',[],'select')
    return cityPeople


