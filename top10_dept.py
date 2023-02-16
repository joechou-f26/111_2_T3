#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 09:01:26 2023

@author: joechou

各校行銷系(或行銷相關系) 學士班(日間) 學生總人數 Top10 系所

"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties #顯示中文字型
myFont=FontProperties(fname='msj.ttf')
# load dataset
df=pd.read_csv('student.csv')  # 106-111 學年度
# set up sidebar margins
padding_top = 0
padding_bottom = 10
padding_left = 1
padding_right = 10
# max_width_str = f'max-width: 100%;'
st.markdown(f'''
            <style>
                .reportview-container .css-1lcbmhc .css-1outpf7 {{
                padding-top: 5px;
                }}
            </style>
            '''
)

st.sidebar.text("台灣大專院校\n相關系所學生人數統計排行")
# filter parameter  
with st.sidebar:
# 學年度
     year_list=df['year'].unique().tolist()
     year_list.sort(reverse=True)
     n_year = st.sidebar.selectbox("選擇年度", year_list, index=0)
# 學制班別
     type_list=df['class_type'].unique().tolist()
     s_type = st.sidebar.selectbox('選擇學制班別', type_list, index=0)
# 相關系所關鍵字
     s_dept = st.text_input('輸入相關系所關鍵字','行銷')
# 排行前幾名
     n_top = st.slider('選擇排行前幾名',3, 30, 10)
# 顯示學生人數
     b_show_num = st.radio('數字資訊', ('學生人數', '人數排名'))
    
# filtering data    
df_filtered = df[(df['year']==n_year) & 
                      (df['dept_name'].str.contains(s_dept)) & 
                      (df['class_type']==s_type)] 
df1=df_filtered.groupby('school_name')['total'].sum().reset_index()
df1=df1.sort_values(by='total',ascending=False).head(n_top)
df1 = df1.iloc[::-1] #為了由大到小畫 barh, 反轉整個 df

#--- plot    
fig=plt.figure(figsize=(12,8))  # set up size of figure
plt.barh(df1.school_name, df1.total)
# plot new xticks and yticks
yticks=df1.school_name.unique()
plt.yticks(yticks, fontproperties=myFont)

# plot title, x/y label, and annotation text
plt.title('{0}學年度({1})台灣大專院校-{2}系(或{3}相關系)-{4}學生總人數 Top{5} 系所'.format(n_year, n_year+1911, s_dept, s_dept, s_type,n_top),fontproperties=myFont, fontsize='x-large')
plt.xlabel('學生總人數',fontproperties=myFont)
# 在 Bar 註明學生人數 或 人數排名
# 在 Bar 註明數量
if b_show_num=='學生人數':
    x_val=df1['total'].values.tolist()
    for i, v in enumerate(x_val):
        plt.text(v, i, '{:,.0f}'.format(v), color='white', horizontalalignment='right', verticalalignment='center', fontsize=8)
elif b_show_num=='人數排名':
     for i in range(n_top):
         plt.text(15, i, '{0}'.format(n_top-i), color='yellow', horizontalalignment='right', verticalalignment='center', fontsize=10) 
plt.tight_layout()
plt.show()

st.pyplot(fig)
