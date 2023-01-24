# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 19:48:40 2023

@author: kmahadevan
"""

import pandas as pd
import numpy as np
import sys

from glob import glob

#This loop helps in combining all the .csv files soil moisture depth values in one dataframe
#glob helps in reading all the csv in one folder with a same pattern
df = pd.concat ([pd.read_csv(one_filename, usecols=['Reading Time (CST)','5 cm Depth Sensor 1 WFV (%)',
                              '5 cm Depth Sensor 2 WFV (%)','5 cm Depth Sensor 3 WFV (%)',
                              '20 cm Depth Sensor 1 WFV (%)','20 cm Depth Sensor 2 WFV (%)',
                              '20 cm Depth Sensor 3 WFV (%)','50 cm Depth Sensor 1 WFV (%)',
                              '50 cm Depth Sensor 2 WFV (%)','50 cm Depth Sensor 3 WFV (%)',
                              '100 cm Depth Sensor 1 WFV (%)','100 cm Depth Sensor 2 WFV (%)',
                              '100 cm Depth Sensor 3 WFV (%)']) 
                 for one_filename in glob('C:/Users/kmahadevan/Downloads/RISMA_4_new/Manitoba_Station4_15MinuteData_*.csv')])  

#converts string date obj to datetime object and creates a new column "DateTime" in df
df["DateTime"] = pd.to_datetime(df["Reading Time (CST)"]) 

#Dropping duplicate since RISMA has first and last dates as duplicates
df = df.drop_duplicates(subset="DateTime", keep="first")

#Resample does most of the job, removes 0:15min, 0:30min & 0:45min and retains only hourly data
#Fills the missing dates and hours with previous row's values
df = df.set_index("DateTime").resample("H").ffill()
df = df.reset_index()

#Dropping only "Reading Time (CST)" since its dtype is creating issues
df = df.drop("Reading Time (CST)", axis="columns")

#Loop to remove "no data" & "No sensor" from the df
for column in df:
    if column != "DateTime":    #if condition to skip time column
        df[column] = np.where((df[column] == "No Data"), np.NaN, df[column])
        df[column] = np.where((df[column] == "No Sensor"), np.NaN, df[column])

#Loop to change the soil moisture depth columns to "float" instead of "object"       
for column_for_avg in df:
    if column_for_avg != "DateTime":  #if condition to skip time column
        df[column_for_avg] =  df[column_for_avg].astype(float)

#Loop to change negative soil moisture values 
for column in df:
    if column != "DateTime":
        df[column] = np.where((df[column] < 0), np.NaN, df[column])

#Avg of 3 sensors for each depth
df["5cm_avg"] = df[["5 cm Depth Sensor 1 WFV (%)","5 cm Depth Sensor 2 WFV (%)","5 cm Depth Sensor 3 WFV (%)"]].mean(axis=1)
df["20cm_avg"] = df[["20 cm Depth Sensor 1 WFV (%)","20 cm Depth Sensor 2 WFV (%)","20 cm Depth Sensor 3 WFV (%)"]].mean(axis=1)
df["50cm_avg"] = df[["50 cm Depth Sensor 1 WFV (%)","50 cm Depth Sensor 2 WFV (%)","50 cm Depth Sensor 3 WFV (%)"]].mean(axis=1)
df["100cm_avg"] = df[["100 cm Depth Sensor 1 WFV (%)","100 cm Depth Sensor 2 WFV (%)","100 cm Depth Sensor 3 WFV (%)"]].mean(axis=1)

#drops unwanted columns after averaging 
df.drop(df.iloc[:, 1:13], inplace=True, axis=1)

#Condition to isolate October to Feburary month's data from 2013-21
count=0
for i in range (2013,2021):
    k = str(i+1)
    j = str(i)
    if count ==0:
        Remove_winter = pd.date_range(start="10-01-" +j, end="03-01-" +k, freq = "H")
        Remove_winter_2 = Remove_winter
        count=1
    else:
        Remove_winter = Remove_winter_2.append(pd.date_range(start="10-01-" +j, end="03-01-" +k, freq = "H")).sort_values()
        Remove_winter_2 = Remove_winter

#Loop to exclude the isolated October to Feburary data 
for i in Remove_winter:
        print(i)
        res = df[~(df["DateTime"] == i)]
        df = res
print(df)

df = df.set_index("DateTime")
                

df.to_csv("C:/Users/kmahadevan/Downloads/RISMA_4_new/combined_data.csv")























