#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:24:00 2023

@author: lilychiou

依地區搜尋104 行政助厘  

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from sqlalchemy import create_engine

login_mysql = "login_mysql.json"  # login mysql user, pw ,  db
with open(login_mysql) as login_mysql:
    login_mysql = json.load(login_mysql)
    

engine_string = "mysql+mysqlconnector://{}:{}@localhost/{}".\
    format(login_mysql['user'], login_mysql['password'] ,login_mysql['database'] )
mysql__engine = create_engine(engine_string)



# 以下  讀取 台灣的地區代碼 for 104
area_txt_file = "area.txt"
df2 = pd.read_csv(area_txt_file)
values=[]  #存 地區 公司名稱 職稱 薪資
    
for  idx in df2.index :

    area_Taiwan = df2['no'][idx]
    des_Taiwan = df2['des'][idx]
    page = 1
       
    while page > 0 :
        url =  'https://www.104.com.tw/jobs/search/?ro=0&kwop=1&\
            keyword=%22%E8%A1%8C%E6%94%BF%E5%8A%A9%E7%90%86%22&\
                expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&\
                    area={}&order=12&asc=0&page={}&mode=s&\
                        jobsource=index_s&langFlag=0&langStatus=0&\
                            recommendJob=1&hotJob=1'.format( area_Taiwan,page)
        
             

        print(url)
        print('-'*80)
              
        resp = requests.get(url)
        
        if resp.status_code == 200:
           soup = BeautifulSoup(resp.text , 'html.parser')
           soup.prettify()
           soup2 = soup.find('div',{'id':'js-job-content'}).\
             findAll('article',{'class':'b-block--top-bord job-list-item b-clearfix js-job-item'})

        counts_per_page = len(soup2)
    
        if counts_per_page > 0:
            page += 1
        else:
            page = 0
        
        # page = 0   測試 單一頁
        i = 0
        
        for job in soup2:
            
            print(des_Taiwan)               #地區名稱
            print(job['data-cust-name'])    #公司名稱
            print(job['data-job-name'])     #職務名稱
            print(job['data-indcat-desc'])  #公司類別
            value=[area_Taiwan,\
                   job['data-cust-name'],\
                   job['data-indcat-desc'],\
                   job['data-job-name']]
    
            """
            area_Taiwan :           104_for_AdminAsst(area_no)  
            job['data-cust-name']:  104_for_AdminAsst(company_name) 
            job['data-indcat-desc']:104_for_AdminAsst(company_type) 
            ob['data-job-name']:    104_for_AdminAsst(job_name)
            """
            
            find_salary_1 = soup2[i].find('div',{'class':'job-list-tag b-content'}).\
                findAll('span',{'class':'b-tag--default'})
            find_salary_2 = soup2[i].find('div',{'class':'job-list-tag b-content'}).\
                findAll('a',{'class':'b-tag--default'})
            tags=[]
    
            try:
                for tag in  find_salary_1:
                    tags.append(tag.text)
                for tag in  find_salary_2:
                    tags.append(tag.text)
    
         
                print(tags[0])  # 薪資
                value.append(tags[0])  # 104_for_AdminAsst(salary)
            except:
                # 找不到薪資待還會出現錯誤 : 'NoneType' object is not iterable
                tags = []
        
        
            i += 1
           
            values.append(value)


columns_name = ['area_no','company_name','company_type','job_name','salary']
df3 = pd.DataFrame()
df3 = pd.DataFrame(values,columns = columns_name )

df3.drop_duplicates(inplace=True)  #刪除重覆資料


df3.to_sql('104_for_AdminAsst', con=mysql__engine, if_exists='append', index=False)

mysql__engine.dispose()  ## disconnect from mysql

