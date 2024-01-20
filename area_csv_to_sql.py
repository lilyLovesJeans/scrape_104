#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 21:29:39 2024

@author: lilychiou

load area.txt and  inert to mysql 104_area table
"""

import pandas as pd
from sqlalchemy import create_engine
mysql__engine = create_engine("mysql+mysqlconnector://python_user:79979898@localhost/scrape_104")

area_txt_file = 'area.txt'
df = pd.read_csv(area_txt_file)

#df = df.loc[:,['no','des','city']]
df= df.rename(columns={"no":"area_no","des":"area_name","city":"city_name"})
df.to_sql('104_area', con=mysql__engine, if_exists='append', index=False)

mysql__engine.dispose()  ## disconnect from mysql

