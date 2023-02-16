#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:03:04 2023

@author: joechou
"""

#----------------------------------------------------------------------
# DV: 台中地區大學人數變化比較 (101-111學年)- line chart
#----------------------------------------------------------------------
#--- data
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties #顯示中文字型
myFont=FontProperties(fname='msj.ttf')

# load dataset
df=pd.read_csv('student.csv')  # 106-111 學年度

#--- set up style of the web page
st.sidebar.text("台中地區的大學人數變化比較(101-111)")

#--- data
# filter parameter  
with st.sidebar:
    options = st.sidebar.multiselect('選擇想要比較的學校：',
        ['逢甲大學', '東海大學', '靜宜大學','亞洲大學',
         '僑光科技大學','嶺東科技大學','朝陽科技大學','中臺科技大學','弘光科技大學',
         '中國醫藥大學','中山醫學大學',
        '國立中興大學','國立臺中教育大學','國立臺中科技大學','國立勤益科技大學','國立臺灣體育運動大學'],
        ['逢甲大學', '東海大學', '靜宜大學'])

df1=df[df.school_name.isin(options)]
df2=df1.groupby(['year','school_name'])['total'].sum().reset_index()
schools=df2.sort_values(by='total', ascending=False)['school_name'].unique().tolist()

#--- plot
fig = plt.figure(figsize=(12,6))  # set up size of figure
year=df1['year'].unique()
xpos = np.arange(len(year))  #將一個指定範圍的值平均分配，然後傳回array
for s in schools:
    df3=df2[df2.school_name==s]
    plt.plot(xpos, df3.total, 'o-', label=s)
plt.title('台中地區大學人數變化比較 (106-111學年)',fontproperties=myFont, fontsize='x-large')
plt.xlabel('學年度',fontproperties=myFont)
plt.ylabel('學生人數',fontproperties=myFont)
# plot new xticks and yticks
plt.xticks(xpos, year, fontproperties=myFont)
ylocs, ylabels = plt.yticks() 
new_yticks=['{0:,}'.format(item) for item in ylocs]
plt.yticks(ylocs, new_yticks)
plt.legend(prop=myFont,loc='upper left') # display legend
plt.show()

st.pyplot(fig)
