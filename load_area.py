#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 19:10:53 2023

@author: lilychiou

讀取104 的地區代碼 ，將屬於台灣地區的代碼存為 area.txt
"""

import json
import pandas as pd

def save_area_for_Taiwan():
    area_json_file = 'area_job104.json'
    
    
    with open(area_json_file) as area : 
        continents = json.load(area)
        
        df1=[]
        for i in continents[0]['n']:  #[0]是台灣地區
            ndf = pd.DataFrame(i['n']) #i 代表台灣地區有 20個縣市 
            ndf['city'] = i['des']  #將[i]的縣市名賦予 city 這個欄位
            df1.append(ndf)
    
    df1= pd.concat(df1,ignore_index=True)
    df1 = df1.loc[:,['city','des','no']]
    df1 = df1.sort_values('no')
    
    
    
    # 以下  讀取 台灣的地區代碼 for 104
    area_file = 'area.txt'
    df1.to_csv(area_file,index=False)
    
    


def get_areaNo():
    area_txt_file = 'area.txt'
    df2 = pd.read_csv(area_txt_file)
    
    for area_Taiwan in df2['no']:
        print(area_Taiwan)
        yield area_Taiwan