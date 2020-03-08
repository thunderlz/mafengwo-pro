#! /bin/python
#通过yjlinks.csv来获取所有的页面
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
import random
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
ffoptions=Options()
ffoptions.add_argument('--headless')
driver=webdriver.Firefox(options=ffoptions)

#获取链接的csv文件
if os.path.exists('yjlinksfetch.csv'):
    df=pd.read_csv('yjlinksfetch.csv',index_col=0)
else:
    df=pd.read_csv('yjlinks.csv',header=None)
    df.columns=['mdd','yjlink']
    df['fetched']=0
    df.to_csv('yjlinksfetch.csv')
dfcopy=df.copy()
    
rootpath='./游记'
if not os.path.exists(rootpath):
    os.mkdir(rootpath)
for index,item in df.iterrows():
    if item[2] == 0:
    #     目的地的目录
        if not os.path.exists(rootpath+'/{}'.format(item[0])):
            os.mkdir(rootpath+'/{}'.format(item[0]))

        #获取攻略页面
        try:
            driver.get(item[1])
            #这是下卷的语句  
            for i in range(2,200):   #也可以设置一个较大的数，一下到底
                js = "var q=document.documentElement.scrollTop={}".format(i*100)  #javascript语句
                driver.execute_script(js)
            time.sleep(random.randint(4,8))
    #             rqgonglve=session.get(item[1],headers=headers,timeout=10)
        except:
            continue
        bsobj=BeautifulSoup(driver.page_source,'lxml')
        try:
            print(item[1],bsobj.title.string)
            # 获取一个网页的源代码和所有的图片保存 网页是bsobj
            with open(rootpath+'/{}/{}.html'.format(item[0],bsobj.title.string),'wt') as f:
                f.write(str(bsobj))
        except:
            print(item[1],'北京',index)
            with open(rootpath+'/{}/北京{}.html'.format(item[0],index),'wt') as f:
                f.write(str(bsobj))
        dfcopy.at[index,'fetched']=1
        dfcopy.to_csv('yjlinksfetch.csv')