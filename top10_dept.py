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

df=pd.read_csv('student.csv')  # 106-111 學年度

#Add sidebar to the app
st.sidebar.markdown("台灣大專院校各相關系所學生人數統計排行")
#Select box   
#col1, col2, col3, col4 = st.sidebar.columns(4)
with st.sidebar:
     year_list=df['year'].unique().tolist()
     year_list.sort(reverse=True)
     n_year = st.sidebar.selectbox("選擇年度", year_list, index=0)

with st.sidebar:
     type_list=df['class_type'].unique().tolist()
     s_type = st.sidebar.selectbox('選擇學制班別', type_list, index=0)

with st.sidebar:
     s_dept = st.text_input('輸入相關系所關鍵字','行銷')

with st.sidebar:
     n_top = st.slider('選擇排行前幾名',3, 20, 10)
     
# filter data    
df_filtered = df[(df['year']==n_year) & 
                      (df['dept_name'].str.contains(s_dept)) & 
                      (df['class_type']==s_type)] 
df1=df_filtered.groupby('school_name')['total'].sum().reset_index()
df1=df1.sort_values(by='total',ascending=False).head(n_top)
df1 = df1.iloc[::-1] #為了由大到小畫 barh, 反轉整個 df

#--- plot    
fig=plt.figure(figsize=(12,6))  # set up size of figure
#plt.style.use('ggplot')
plt.barh(df1.school_name, df1.total)
# plot new xticks and yticks
yticks=df1.school_name.unique()
plt.yticks(yticks, fontproperties=myFont)

# plot title, x/y label, and annotation text
plt.title('{0}學年度台灣大專院校-{1}系(或{2}相關系)-{3}學生總人數 Top{4} 系所'.format(n_year, s_dept, s_dept, s_type,n_top),fontproperties=myFont)
plt.xlabel('學生總人數',fontproperties=myFont)
# 在 Bar 註明數量
y_val=df1['total'].values.tolist()
for i, v in enumerate(y_val):
    plt.text(v, i, '{:,.0f}'.format(v), color='white', horizontalalignment='right', verticalalignment='center', fontsize=8)
plt.tight_layout()
plt.show()

st.pyplot(fig)
