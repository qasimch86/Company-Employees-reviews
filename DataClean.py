# -*- coding: utf-8 -*-
"""
Created on Friday August 24 16:00 2018

@author: Qasim Ali
"""

"""
Objective: To perform the data preprocessing to prepare the data for analysis
Packages: Numpy, Pandas, OS, Matplotlib, Seaborn
"""

# Set your working directory with os.chdir()
# importing packages required for manipulating the data 

import pandas as pd
from collections import OrderedDict
import os
import numpy as np
import math as mt
os.chdir('/Users/ABCD/data')

# Created a for loop to read all 100 excel files and then the variable names were renamed and saved into empty dataframe named "new_df". "Parse_date"
# was used to parse string into datetime objects. The next for loop were used to fetch and assign all 14 survey questions and answers into the column 
# 'Question' and 'Answer' respectively in the dataframe "new_df". Then the dataframe "comb_df" and "new_df" were concatenated by using concat() 
# function in a data frame called "comb_df". There were 22226 rows and 32 columns in the data frame "comb_df". The attribute 'FacID' is a unique 
# factory identifier, 'UserID' is a unique worker identifier,'TimeStamp' is the time when workers recorded the answers to survey questions, Duration'
# is the duration of the worker call in seconds to answer survey questions.


comb_df=pd.DataFrame()
for i in range(1,101):
    f_name='Data'+str(i)+'.xlsx'
    df=pd.read_excel(f_name, sheet_name='Branch'+str(i),parse_date=['SurveyTime'])
    new_df=pd.DataFrame({'BranchID':df.BranchID,'EmployeeID':df.EmployID,'SurveyTime': df.SurveyTime,
                        'PerformanceScore':df.PerformanceScore})
    for j in range(1,7):
        new_df['Query'+str(j)]=df['SurveyQuestion'+str(j)]
        new_df['Response'+str(j)]=df['Answer'+str(j)]
    comb_df=pd.concat([comb_df,new_df], ignore_index=True)

# Each survey questions column contains more than one questions and their answers. This lead to the problem of containing both numeric and text 
# responses in each column. To address this, the unique questions from all 14 questions column were identified then duplicate questions were removed
# and saved in dataframe "Q".

Qs=[];
for i in range(1,7):
    Qs.append(comb_df['Query'+str(i)].unique())
Q=pd.DataFrame({'Col1': np.concatenate(Qs)}).Col1.unique()
# len(Q),Q

# This is important because python cannot convert string to float if only one non nan query present in the statement.
comb_df=comb_df.replace(Q[5],'')

# The irrelevant questions were removed. The unique or inconsistent questions in each column from dataframe "Q" were stacked with the most frequent 
# questions in each question column so that same questions are combined in each column across 14 question column. After sorting, the questions were
# saved in array "Q_uniq".

arr_irrv=[4,5,6,7,9,11,12,13,14,15,16]#Remove non-interested questions/strings from array Q
Q_uniq=np.delete(Q,arr_irrv)#Delete non-valid questions but unsorted
len(Q_uniq),Q_uniq

# Here we are replacing irrelevant queries in each column of the dataframe by empty string '' so that each query column should have the specific question in it. Let's remember this step as (*)

for i in range(0,len(Q_uniq)):
    comb_df['Response'+str(i+1)]= comb_df['Response'+str(i+1)].replace(comb_df['Response'+str(i+1)][comb_df['Query'+str(i+1)]!=Q_uniq[i]],'')
    comb_df['Query'+str(i+1)]= comb_df['Query'+str(i+1)].replace(comb_df['Query'+str(i+1)][comb_df['Query'+str(i+1)]!=Q_uniq[i]],'')

# This step is performed to sort data in ascending order according to the null values in the row.

Null_arr=[];
df_Qsort=comb_df
for i in range(0,len(comb_df)):
    Null_arr.append(sum(df_Qsort.iloc[i,:]==''))
df_Qsort['Null_values']=pd.DataFrame({'Null_values':Null_arr}).values
Sorted_df=df_Qsort.sort_values('Null_values',ascending=True)#df_Qsort

del df_Qsort['Null_values']
del Sorted_df['Null_values']

#The above step involves loss of information that is in irrlevant column. It is possible that the irrelevant information in one column is relevant in the other column. Therefore step (*) can be replaced by the following code to reduce information loss.

# Irrelevant questions that were not present in Q_uniq array were removed from the data and the values were replaced by empty string

#for i in arr_irrv:
#    comb_df=comb_df.replace(Q[i],'')


## Now each observation in the question columns were checked and question columns were concatenated so that similar questions are in the same column. 
#c=len(comb_df.iloc[0])#Total number of columns
#r=len(comb_df)#Total number of rows
#df_Qsort=pd.DataFrame()
#df_Qsort=pd.concat([df_Qsort,comb_df])
#X=[];
#print(c,r)
#for k in range(0,r):
#    ii=0
##     print(k,end=",",flush=True)
#    for i in range(4,c,2):
#        for j in range(4,c,2):
#            if comb_df.iloc[k,j]==Q_uniq[ii]:
#                    df_Qsort.iloc[k,i]=comb_df.iloc[k,j]
#                    df_Qsort.iloc[k,i+1]=comb_df.iloc[k,j+1]
#                    if i!=j:
#                        df_Qsort.iloc[k,j]=""
#                        df_Qsort.iloc[k,j+1]=""
#        ii=ii+1
#    X.append(sum(df_Qsort.iloc[k,4:]==''))
#df_Qsort['Null_values']=pd.DataFrame({'Null_values':X}).values
#Sorted_df=df_Qsort.sort_values('Null_values',ascending=True)#df_Qsort

##del df_Qsort['Null_values']
##del Sorted_df['Null_values']

# Now we can see first four columns are reserved while next are Queries and their responses.
# We want to delete all those rows that have 1 or 2 responses. This means Y<10.
# Since we have already arranged the data set, we can delete the required rows easily

Y=np.sort(Null_arr)
comb_df2=Sorted_df.drop(Sorted_df.index[Y>10])


# Finally the data was exported in an excel sheet

writer=pd.ExcelWriter('Combined.xlsx')
comb_df2.to_excel(writer,'Sheet1')
writer.save()

# Reading the data again so that above steps can be skipped
comb_df2=pd.DataFrame()
f_name='Combined.xlsx'
comb_df2=pd.read_excel(f_name,parse_date=['SurveyTime'])

# Queries are named by their keywords. No long sentences needed
Questions=[];
Questions.append('Wages')
Questions.append('Fire Safety')
Questions.append('Abuse')
Questions.append('Child Labor')
Questions.append('Worker Voluntary Feedback')
Questions.append('Worker Recommendation')
len(Questions),Questions[0],Questions[5]


# Queries are replaced by query keywords (Questions) and set as the column heads and the responses are set as values below the query keywords (head). data is split into two dataframes as per their category.

c=len(comb_df2.iloc[0])#Total number of columns
split_q={}
df_id={}
split_df={}
for i in range(0,2):
    df_id[i]= pd.DataFrame({'BranchID':comb_df2.BranchID,'EmployeeID':comb_df2.EmployeeID,'SurveyTime': comb_df2.SurveyTime,
                'PerformanceScore':comb_df2.PerformanceScore})
split_q[0]=pd.DataFrame({Questions[0]:comb_df2.Response1, Questions[1]:comb_df2.Response2,
                         Questions[2]:comb_df2.Response3, Questions[3]:comb_df2.Response4})
split_q[1]=pd.DataFrame({Questions[4]:comb_df2.Response4, Questions[5]:comb_df2.Response5})
for i in range(0,2):
    split_df[i]=pd.concat([df_id[i],split_q[i]],axis=1, sort=False)

# null values in each row are summed-up to sort the data in ascending order
r=len(comb_df2)#Total number of rows
X=[]
Y=[]
for k in range(0,r):
    X.append(sum(split_df[0].iloc[k,4:].isnull()))
    Y.append(sum(split_df[1].iloc[k,4:].isnull()))

split_df[0]['Null_values']=pd.DataFrame({'Null_values':X}).values
split_df[1]['Null_values']=pd.DataFrame({'Null_values':Y}).values
SrtSplt_df={}
SrtSplt_df[0]=split_df[0].sort_values('Null_values',ascending=True)#df_Qsort
SrtSplt_df[1]=split_df[1].sort_values('Null_values',ascending=True)#df_Qsort

# Data sorted and null values column deleted.
Srtd_Splt_df={}
X1=np.sort(X)
Y1=np.sort(Y)
Srtd_Splt_df[0]=SrtSplt_df[0].drop(SrtSplt_df[0].index[X1>4])
Srtd_Splt_df[1]=SrtSplt_df[1].drop(SrtSplt_df[1].index[Y1>2])

del Srtd_Splt_df[0]['Null_values']
del Srtd_Splt_df[1]['Null_values']

# Finding median of the data so that missing values can be replaced by median values

median_Q=[];
for i in range(0,6):
    if i<4:
        median_Q.append(Srtd_Splt_df[0][Srtd_Splt_df[0][Questions[i]].notnull()][Questions[i]].median())
        Srtd_Splt_df[0][Questions[i]]=Srtd_Splt_df[0][Questions[i]].replace(mt.nan,median_Q[i])
    elif i<6:
        median_Q.append(Srtd_Splt_df[1][Srtd_Splt_df[1][Questions[i]].notnull()][Questions[i]].median())
        Srtd_Splt_df[1][Questions[i]]=Srtd_Splt_df[1][Questions[i]].replace(mt.nan,median_Q[i])
        
#Saving data in to two sheets
writer=pd.ExcelWriter('Combined5.xlsx')
Srtd_Splt_df[0].to_excel(writer,'Sheet1')
Srtd_Splt_df[1].to_excel(writer,'Sheet2')
writer.save()

#Remember that there are 100 branches of the company. Here for each branch, all responses are collected and their positive responses are proportioned.
l=np.array([4,2]);
Qprop_df=np.empty((100,2,6),dtype=float);
for i in range(0,100):
    for j in range(0,2):
        if sum(Srtd_Splt_df[j].BranchID.unique()=='Branch'+str(i+1))==1:
            for k in range(0,sum(l)):
                if sum(Srtd_Splt_df[j].columns==Questions[k])==1:
                    m1=0;m2=0;
                    m1=sum(Srtd_Splt_df[j][Srtd_Splt_df[j][Questions[k]]==1]['BranchID']=='Branch'+str(i+1))
                    m2=sum(Srtd_Splt_df[j][Srtd_Splt_df[j][Questions[k]]==2]['BranchID']=='Branch'+str(i+1))
                    if m1+m2!=0:
                        Qprop_df[i,j,k]=m1/(m1+m2)
                    else:
                        Qprop_df[i,j,k]=''


#Data is set with each Branch ID and saved to Combined.xlsx
Fac_df={}
Fac_df[0]=pd.DataFrame({'BranchID':np.array(range(1,101)),Questions[0]:Qprop_df[:,0,0],Questions[1]:Qprop_df[:,0,1],Questions[2]:Qprop_df[:,0,2],
                       Questions[3]:Qprop_df[:,0,3]})

Fac_df[1]=pd.DataFrame({'BranchID':np.array(range(1,101)),Questions[4]:Qprop_df[:,1,4],Questions[5]:Qprop_df[:,1,5]})

for i in range(0,2):
    for j in range(0,100):
        Fac_df[i]['BranchID']=Fac_df[i]['BranchID'].replace(j,'Branch'+str(j))
        
writer=pd.ExcelWriter('Combined.xlsx')
Fac_df[0].to_excel(writer,'Sheet1')
Fac_df[1].to_excel(writer,'Sheet2')
writer.save()

# The data is fully preprocessed and now ready to be analysed.

#Good Luck!