   # -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 10:50:32 2017

@author: yunyangye
"""

import multiprocessing as mp
import time
import math
import csv
import subprocess
from shutil import copyfile,rmtree
import pandas as pd
import numpy as np
import os.path
from bs4 import BeautifulSoup

######################################################


def modifyIDF(climate,param_value,order_model,model_type,schedule):
    f = open('./SourceFolder/'+model_type+'/'+climate+'.idf','rb')
    lines=f.readlines()
    f.close()
    
    newlines = []
    modify_id = []
    
    newlines = []
    for i in range(len(lines)):
        #this line need to be modified for differnt builidng
        if lines[i].split(',')[0].replace(' ','') == 'ElectricEquipment'and lines[i+3].split(',')[0].replace(' ','')==schedule:
            modify_id.append(i+6)
                    
    for i in range(len(lines)):
        if i in modify_id:
            newlines.append('  '+str(param_value[0])+',                       !- Watts per Zone Floor Area {W/m2}\n')
        else:
            newlines.append(lines[i])
            
    f = open('./'+model_type+'/'+climate+str(order_model)+'.idf','w')
    for i in range(len(newlines)):
        f.writelines(newlines[i])
    f.close()       
    return str(order_model)+'.idf'     


######################################################
#2.modify IDF file and run model, get model output (site EUI)
#run models and read htm file to get site EUI and source EUI
#save the model input and output into './results/energy_data.csv'
def runModel(climate,model_type,eplus_path,weather_file,eplus_file,param_value,output_file,output):
    #run model
    df = subprocess.Popen([eplus_path, "-w",weather_file, "-d",'./results/'+climate+output_file+eplus_file.split('.')[0], "-r", './'+model_type+'/'+climate+eplus_file],stdout=subprocess.PIPE)
    output_eplus, err = df.communicate()
    print(output_eplus.decode('utf_8'))
    if not err is None:
        print(err.decode('utf_8'))
    
    if os.path.isfile('./results/'+climate+output_file+eplus_file.split('.')[0]+'/eplustbl.htm'):
         #get model input
        data = []
        data.append(eplus_file.split('.')[0]) #the name of idf file
        data.append(climate) #the name of climate
        data.append(param_value[0])
        
        #get output(site EUI and source EUI)
        path='./results/'+climate+output_file+eplus_file.split('.')[0]+'/eplustbl.htm'
        with open(path) as fp:
            soup = BeautifulSoup(fp)

        energy_table = soup.find_all('table')[0]
        rows = energy_table.find_all('tr')
        total_site_energy_data = rows[1]
        total_source_energy_data = rows[3]
        total_site_energy_per_total_building_area_html = total_site_energy_data.find_all('td')[2]
        total_source_energy_per_total_building_area_html = total_source_energy_data.find_all('td')[2]
        total_site_energy_per_total_building_area = float(total_site_energy_per_total_building_area_html.text)*0.088055066
        total_source_energy_per_total_building_area= float(total_source_energy_per_total_building_area_html.text)*0.088055066
        data.append(total_site_energy_per_total_building_area)
        data.append(total_source_energy_per_total_building_area)
    
        #record the data in the './results/energy_data.csv'
        with open(model_type+'_energy_data.csv', 'ab') as csvfile:
            energy_data = csv.writer(csvfile, delimiter=',')
            energy_data.writerow(data)

    else:
        with open('./results/energy_data_err.csv', 'ab') as csvfile:
            energy_data_err = csv.writer(csvfile, delimiter=',')
            energy_data_err.writerow(climate+eplus_file)
            
    while 1:
        try:
            rmtree('./results/'+climate+output_file+eplus_file.split('.')[0])
            break
        except:
            pass
        
    output.put([])
 
           


#################################################################################
#2.modify IDF file and run model, get model output (site EUI)
#run models in parallel for sensitivity analysis
#Climate is the list of climate zone; weather file name is [climate].epw and baseline model file name is CZ[climate].osm
#round_num is the number of the round times
def parallelSimu(climate,round_num,model_type,schedule):
    #record the start time
    start = time.time()
    #eplus_path ='/usr/EnergyPlus/energyplus-8.7.0'
    eplus_path ='energyplus'
    weather_file ='./SourceFolder/'+climate+'.epw'
    output_file = 'temp'
    # get parameter value    
    param_value = []
        
    with open('./model_inputs.csv', 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            param_value.append(row)
    
    # modify the idf file
    order_idf = 1
    for i in range(len(param_value)):
        modifyIDF(climate,param_value[i],order_idf,model_type,schedule)
        order_idf += 1
        
    # idf file name    
    order_model = 1    
    eplus_files = []
    for i in range(len(param_value)):
        eplus_files.append(str(order_model)+'.idf')
        order_model +=1   
            
    #multi-processing
    output = mp.Queue()
    processes = [mp.Process(target=runModel,args=(climate,model_type,eplus_path,weather_file,eplus_files[i],param_value[i],output_file,output)) for i in range(len(eplus_files))]
    
    #count the number of cpu
    cpu = mp.cpu_count()#record the results including inputs and outputs
    print cpu
    
    model_results = []
    
    run_times = math.floor(len(processes)/cpu)
    if run_times > 0:
        for i in range(int(run_times)):
            for p in processes[i*int(cpu):(i+1)*int(cpu)]:
                p.start()
            
            for p in processes[i*int(cpu):(i+1)*int(cpu)]:
                p.join()
    
            #get the outputs
            temp = [output.get() for p in processes[i*int(cpu):(i+1)*int(cpu)]]
            
            for x in temp:
                model_results.append(x)
    
    for p in processes[int(run_times)*int(cpu):len(processes)]:
        p.start()
            
    for p in processes[int(run_times)*int(cpu):len(processes)]:
        p.join()    
        
    #get the outputs
    temp = [output.get() for p in processes[int(run_times)*int(cpu):len(processes)]]
    for x in temp:
        model_results.append(x)
            
    #record the end time
    end = time.time()
    return model_results,end-start
