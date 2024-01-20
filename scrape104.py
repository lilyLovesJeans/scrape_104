#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:24:00 2023

@author: lilychiou

搜尋104 行政助厘 職位 jobcat=2002001012

"""

import requests

from bs4 import BeautifulSoup

import pandas as pd
from sqlalchemy import create_engine
mysql__engine = create_engine("mysql+mysqlconnector://python_user:79979898@localhost/scrape_104")



# 以下  讀取 台灣的地區代碼 for 104
area_txt_file = 'area.txt'
df2 = pd.read_csv(area_txt_file)
values=[]  #存 地區 公司名稱 職稱 薪資
    
for  idx in df2.index :

    area_Taiwan = df2['no'][idx]
    des_Taiwan = df2['des'][idx]
    page = 1
       
    while page > 0 :
        url = 'https://www.104.com.tw/jobs/search/?ro=0&jobcat=2002001012&\
            expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area={}&\
                order=14&asc=0&page={}&mode=s&jobsource=2018indexpoc&langFlag=0&\
                    langStatus=0&recommendJob=1&hotJob=1'.format( area_Taiwan,page)
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
            
            print(des_Taiwan)
            print(job['data-cust-name'])
            print(job['data-job-name'])
            print(job['data-indcat-desc'])
            value=[area_Taiwan,\
                   job['data-cust-name'],\
                   job['data-job-name']]
    
            
            
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
    
                #tags = [tag.text for tag in soup2[i].find('div',{'class':'job-list-tag b-content'}).\
                #        find('a',{'class':'b-tag--default'}) ]  # 舊的寫法 生成式迴圈
                print(tags[0])
                value.append(tags[0])
            except:
                # 找不到薪資待還會出現錯誤 : 'NoneType' object is not iterable
                tags = []
        
        
            i += 1
           
            values.append(value)

# scrape_104_file = 'scrape_104.txt'
columns_name = ['area_no','company_name','job_name','salary']
df3 = pd.DataFrame()
df3 = pd.DataFrame(values,columns = columns_name )
# df3.to_csv(scrape_104_file,index=False)


# scrape_duplicate_file= 'scrape_104_duplicate.txt'
# column_names= ['company_name','job_name','salary']
# df_duplicated= df3[df3.duplicated(subset=column_names,keep=False)]
# df_duplicated.to_csv(scrape_duplicate_file,index=False)
df3.drop_duplicates(inplace=True)  #刪除重覆資料


df3.to_sql('104_for_2002001012', con=mysql__engine, if_exists='append', index=False)

mysql__engine.dispose()  ## disconnect from mysql

