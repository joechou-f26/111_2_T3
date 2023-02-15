#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 22:30:47 2023

@author: joechou

Web App (by streamlit)

=> Male vs. Female ratio pie chart
 
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties #顯示中文字型
myFont=FontProperties(fname='msj.ttf')

df=pd.read_csv('student.csv')  # 106-111 學年度

#Add sidebar to the app
st.sidebar.markdown("台灣大專院校學生人數統計")
#Select box   
col1, col2 = st.columns(2)
with col1:
     year_list=df['year'].unique().tolist()
     year_list.sort(reverse=True)
     n_year = st.selectbox("選擇年度", year_list, index=0)

with col2:
     s_school = st.selectbox(
                "選擇學校", ['逢甲大學', '東海大學', '靜宜大學','國立中興大學','東吳大學','國立臺灣大學'] , index=0)
# filter data    
year=n_year
s_school=s_school
df_filterd = df[(df.year==year) & (df.school_name==s_school)] # all '111年度' records

#--- prepare data
girl=df_filterd.female.sum()
boy=df_filterd.male.sum()
labels = ['男生','女生']
amounts=[]
amounts.extend([boy, girl])

#--- plot
fig = plt.figure(figsize=(8,6))  # set up size of figure
plt.pie(
        amounts,
        labels = labels,
        labeldistance = 1.05,  #項目標題與圓心的距離，是半徑的幾倍 (1.2表示1.2倍)
        autopct =lambda p: '{0:.1f}%({1:.0f})'.format(p, p*sum(amounts)/100),
        #shadow = True,        #True 表示圖形有陰影
        startangle = 90,       #開始繪圖的起始角度
        pctdistance = 0.6,     #百分比文字與圓心的距離是半徑的多少倍
        textprops={'fontproperties': myFont} #設定標籤為中文字.沒這一行會有亂碼
        )
plt.axis("equal")  # 預設為橢圓形，equal為正圓形
plt.title('{0}{1}學年度男女生人數比例'.format(s_school, year),fontproperties=myFont, fontsize='x-large')
plt.legend(prop=myFont) # display legend
plt.tight_layout()
plt.show()

st.pyplot(fig)
