import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import os
import time
import pandas as pd
# https://www.lagou.com/wn/jobs?fromSearch=true&kd=java&city=%E5%8C%97%E4%BA%AC&pn=1
# service = Service('./chromedriver.exe')
# option = webdriver.ChromeOptions()
# browser = webdriver.Chrome(service=service,options=option)
# browser.get('http://www.taobao.com')


class spider(object):
    def __init__(self,type,city,page):
        self.type = type
        self.city = city
        self.page = page
        self.spiderUrl = 'https://www.lagou.com/wn/jobs?fromSearch=true&kd=%s&city=%s&pn=%s'


    def startBrowser(self):
        service = Service('./chromedriver.exe')
        option = webdriver.ChromeOptions()
        option.debugger_address = 'localhost:9222'#把已登录记录保存
        browser = webdriver.Chrome(service=service, options=option)
        return browser

    def main(self,page):
        if self.page > page: return
        print(self.page)
        browser = self.startBrowser()
        print("正在爬取页码路径:"+self.spiderUrl%(self.type,self.city,self.page))
        browser.get(self.spiderUrl%(self.type,self.city,self.page))
        time.sleep(1)
        # // *[ @ id = "jobList"] / div[1] / div[1]
        job_list = browser.find_elements(by=By.XPATH,value='//div[@id="jobList"]/div[@class="list__YibNq"]/div[@class="item__10RTO"]')
        print(job_list)
        print(len(job_list))
        for index,job in enumerate(job_list):
           try:
               # title
               title = job.find_element(by=By.XPATH, value='.//div[@class="p-top__1F7CL"]/a').text
               # companyTitle
               companyTitle = job.find_element(by=By.XPATH, value='.//div[@class="company-name__2-SjF"]/a').text
               # salary
               salary = job.find_element(by=By.XPATH, value='.//div[@class="p-bom__JlNur"]/span').text
               salary = re.findall('\d+', salary)
               minSalary = int(salary[0]) * 1000
               maxSalary = int(salary[1]) * 1000

               # workExperience
               # education
               double = job.find_element(by=By.XPATH, value='.//div[@class="p-bom__JlNur"]').get_attribute(
                   'textContent').split('/')
               workExperience = double[0].split('k')[2].strip()
               education = double[1].strip()
               # totalTag
               try:
                   totalTag = job.find_element(by=By.XPATH,
                                               value='.//div[@class="company__2EsC8"]/div[@class="industry__1HBkr"]').text
                   companyPeople = re.findall('\d+', totalTag)
               except:
                   totalTag = '无'
                   companyPeople = [10]
               try:
                   # companyPeople[1]
                   companyPeople = '-'.join(companyPeople)
               except:
                   companyPeople = companyPeople[0]

               # tagList
               tagList = job.find_elements(by=By.XPATH, value='.//div[@class="ir___QwEG"]/span')
               tagData = []
               for tag in tagList:
                   print(tag.text)
                   tagData.append(tag.text)
               workTag = '/'.join(tagData)
               print(workTag)

               # welfare
               try:
                   welfare = job.find_element(by=By.XPATH,
                                              value='.//div[@class="item-bom__cTJhu"]/div[@class="il__3lk85"]').text.replace(
                       '“', "")
                   welfare = welfare.replace('”', "")
               except:
                   welfare = '无'

               imgSrc = job.find_element(by=By.XPATH, value='.//div[@class="com-logo__1QOwC"]/img').get_attribute("src")
               print(imgSrc)
               print(title, companyTitle, minSalary, maxSalary, workExperience, education, totalTag, companyPeople,
                     workTag, welfare)

               # break
               self.save_to_csv(
                   [self.type, title, companyTitle, minSalary, maxSalary, workExperience, education, totalTag,
                    companyPeople, workTag, welfare, imgSrc, self.city])
               # break
           except:
               continue

        self.page += 1
        time.sleep(5)
        self.main(page)


    def save_to_csv(self,rowData):
        with open('./jobData.csv','a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(rowData)

    def init(self):
        if not os.path.exists('./jobData.csv'):
            with open('./jobData.csv','w',encoding='utf-8',newline='') as wf:
                writer = csv.writer(wf)
                writer.writerow([
                    'type', 'title', 'companyTitle', 'minSalary', 'maxSalary', 'workExperience', 'education',
                    'totalTag', 'companyPeople', 'workTag',
                    'welfare', 'imgSrc', 'city'
                ])



if __name__ == "__main__":

    # spiderObj.init()
    #
    cityList = ['北京','上海','深圳','广州','杭州','北京','上海','深圳','广州','杭州','成都','南京','武汉','西安','厦门','长沙','南昌','苏州','天津',]
    # 'java','web前端','数据分析师','C语言','php开发','php开发',
    typeList = ['IT运维','微信小程序','.Net']
    for city in cityList:
        spiderObj = spider('IT运维', city, 1)
        spiderObj.main(10)
