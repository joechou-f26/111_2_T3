#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:37:38 2023

@author: joechou

Change of student number in two units

"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties #顯示中文字型
myFont=FontProperties(fname='msj.ttf')

# load dataset
df=pd.read_csv('student.csv')  # 106-111 學年度

#--- set up style of the web page
st.sidebar.text("台灣大專院校學生人數統計排行")

#--- data
# filter parameter  
with st.sidebar:
# 學年度
     school=df['school_name'].unique().tolist()
     s_school = st.sidebar.selectbox("選擇學校：", school, index=0)
# 學制班別
     b_pct_change = st.checkbox('顯示變化百分比%')
# filtering data     
df_filtered=df[df.school_name==s_school] 

df1=df_filtered.groupby('year')['total'].sum().reset_index()
df1['total_pchg']=df1['total'].pct_change()    # pct change between two rows
df1['total_pchg'] = df1['total_pchg'].fillna(0) # fill NAN with 0
year=df1['year'].unique()
xpos = np.arange(len(year))  # for positioning x axis
     
#--- plot 
fig, ax1 = plt.subplots(figsize=(11,7)) 
# first axes with unit 'person'
ax1.bar(xpos, df1.total, label='學生人數') 
ax1.set_xlabel('學年度',fontproperties=myFont)  
ax1.set_ylabel('人數', color='tab:blue',fontproperties=myFont, fontsize='large') 
plt.title('{0}學生總人數趨勢 (106-111學年)'.format(s_school),fontproperties=myFont,fontsize='x-large')
ax1.legend(loc="upper left",prop=myFont) 
if b_pct_change:
    # second axes with unit 'change %'
    ax2 = ax1.twinx()  # Create a twin Axes sharing the xaxis
    ax2.plot(xpos, df1.total_pchg, 'or-', label='增減比例') 
    ax2.set_ylabel('人數', color='tab:red',fontproperties=myFont, fontsize='large')  
    ax2.legend(loc="upper right",prop=myFont)  
# plot new xticks and yticks of axis 1, axis 2
plt.xticks(xpos, year, fontproperties=myFont)
ylocs1 = ax1.get_yticks() 
new_yticks1=['{0:,}'.format(item) for item in ylocs1]
ax1.set_yticks(ylocs1)
ax1.set_yticklabels(new_yticks1)
if b_pct_change:
    ylocs2 = ax2.get_yticks() 
    new_yticks2=['{0:,}%'.format(item) for item in ylocs2]
    ax2.set_yticks(ylocs2)
    ax2.set_yticklabels(new_yticks2)
# 在 bar & line 上方註明數量
y_val=df1['total'].values.tolist()
for i, v in enumerate(y_val):
    ax1.text(i,v, '{:,.0f}'.format(v), color='tab:blue', horizontalalignment='center')
y_val=df1['total_pchg'].values.tolist()
if b_pct_change:
    for i, v in enumerate(y_val):
        ax2.text(i,v,  '{:,.0f}'.format(v), color='tag:red', horizontalalignment='right')
plt.show()

st.pyplot(fig)
