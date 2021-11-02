# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 12:14:08 2020

@author: yinglilou
"""
import csv
import pyDOE as doe
from shutil import rmtree

climate = ['1A','2A','2B','3A','3B','3C','4A','4B','4C','5A','5B','6A','6B','7A','8A']
num_sample=50 # the amount of sample
num_sens=1 # the number of model inputs
min_value=8.072933 #the min value of plug load density (W/m2)
max_value=18.94448 #the max value of plug load density (W/m2)
ASHRAEModel_schedule='Worship_MEETING_EQP_SCH'
bEQ_schedule='Worship_MEETING_EQP_SCH''

######################################################################################
#1.sampleing: get different value of model input (LHM)
#s#elect the samples
sample_temp = doe.lhs(num_sens, samples=num_sample)    
param_values = []
for row1 in sample_temp:
    temp = []
    temp.append((max_value-min_value)*row1[0]+min_value)                
    param_values.append(temp)
    
##write sample values in csv
with open('model_inputs.csv', 'wb') as csvfile:
    for row in param_values:
        data = csv.writer(csvfile, delimiter=',')
        data.writerow(row)

###################################################################################
#2.modify IDF file and run model, get model output (site EUI and source EUI)
import parallelSimuMeta as ps

for cz in climate:
    model_results,run_time = ps.parallelSimu(cz,1,'bEQModel_pre',bEQ_schedule)
print run_time
rmtree('./bEQModel_pre')

for cz in climate:
    model_results,run_time = ps.parallelSimu(cz,1,'bEQModel_post',bEQ_schedule)
print run_time
rmtree('./bEQModel_post')

for cz in climate:
    model_results,run_time = ps.parallelSimu(cz,1,'ASHRAEModel',ASHRAEModel_schedule)
print run_time
rmtree('./ASHRAEModel')
