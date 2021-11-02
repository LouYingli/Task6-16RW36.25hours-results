# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 17:22:42 2017

@author: yunyangye
"""
import csv
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import xlsxwriter
  
######################################################
#plot figure
######################################################
def plotDiff(Intercept1,Coef1,Intercept2,Coef2,vintage):
    plt.rcParams["font.family"] = "Times New Roman"

    cz = ['1A','2A','2B','3A','3B','3C','4A','4B','4C','5A','5B','6A','6B','7A','8A']

    Y1_model = []# site EUI (model)
    Y1_calc = []# site EUI (calculate)
    Y2_model = []# source EUI (model)
    Y2_calc =[]# source EUI (calculate)    

    # get ASHRAE EUI from csv
    with open('./ASHRAEModel_energy_data.csv','r') as f:
        temp = list(csv.reader(f,delimiter=','))
    X_ASHRAE = []
    for row in temp:
        temp=[]
        temp.append(row[1]) #climate
        temp.append(float(row[3]))# site EUI
        temp.append(float(row[4])) #source EUI
        X_ASHRAE.append(temp)

    # get beQ EUI from csv
    with open('./bEQModel_'+vintage+'_energy_data.csv','r') as f:
        temp = list(csv.reader(f,delimiter=','))
    for row in temp:
        Y1_model.append(float(row[3]))# site EUI
        Y2_model.append(float(row[4])) #source EUI

    # calculated bEQ baseline
    for row in X_ASHRAE:        
        for ind,x in enumerate(cz):
            if row[0] == x:
                ind_cz = ind
            
        Y1_calc.append(Intercept1[ind_cz]+Coef1[ind_cz]*row[1])
        Y2_calc.append(Intercept2[ind_cz]+Coef2[ind_cz]*row[2])    

    Y1_err = []  
    Y2_err = []
    for i in range(len(Y1_model)):
        Y1_err.append(abs(Y1_calc[i]-Y1_model[i])/Y1_model[i])
        Y2_err.append(abs(Y2_calc[i]-Y2_model[i])/Y2_model[i])
    print max(Y1_err)    
    print max(Y2_err)

        
    #draw the line to express Y1_model = Y1_calc
    n1 = 151
    n2 = 451
    
    cent_line1 = range(0,n1)
    cent_line2 = range(0,n2)
    
    #draw the line to express 10% error
    err_1 = []
    for i in range(0,n1):
        err_1.append(0.9*i)

    err_2 = []
    for i in range(0,n2):
        err_2.append(0.9*i)
    
    # plot the figures for pre-1980
    plt.subplot(211)
    plt.scatter(Y1_model,Y1_calc,marker = '.',s = 5,c = 'r')
    plt.plot(cent_line1,cent_line1,'k')
    plt.plot(cent_line1,err_1,'k--')
    plt.plot(err_1,cent_line1,'k--')

    plt.xlabel('Modeled bEQ baseline site EUI '+r'(kBTU/ft$^2$)')
    plt.ylabel('Calculated bEQ baseline'+'\n'+'site EUI '+r'(kBTU/ft$^2$)')
    plt.text(50,110,'Relative Error = 10%',rotation=20)
    plt.text(55,70,'Relative Error = 10%',rotation=18)
    
    plt.xlim([0,150])
    plt.ylim([0,150])
    
    plt.subplot(212)
    plt.scatter(Y2_model,Y2_calc,marker = '.',s = 5,c = 'r')
    plt.plot(cent_line2,cent_line2,'k')
    plt.plot(cent_line2,err_2,'k--')
    plt.plot(err_2,cent_line2,'k--')

    plt.xlabel('Modeled bEQ baseline source EUI '+r'(kBTU/ft$^2$)')
    plt.ylabel('Calculated bEQ baseline'+'\n'+'source EUI '+r'(kBTU/ft$^2$)')
    plt.text(150,320,'Relative Error = 10%',rotation=20)
    plt.text(160,210,'Relative Error = 10%',rotation=18)
    
    plt.xlim([0,450])
    plt.ylim([0,450])
    
    plt.tight_layout() 
    plt.savefig('regression_'+vintage+'.png')
    plt.show()

    
###################################################################################

cz = ['1A','2A','2B','3A','3B','3C','4A','4B','4C','5A','5B','6A','6B','7A','8A']

Intercept1 = []#pre site EUI
Coef1 = []#pre site EUI
Intercept2 = []#pre source EUI
Coef2 = []#pre source EUI
Intercept3 = []#post site EUI
Coef3 = []#post site EUI
Intercept4 = []#post source EUI
Coef4 = []#post source EUI

    
with open('./inter_coef.csv','r') as f:
    temp = list(csv.reader(f,delimiter=','))
Intercept1 = []#pre site EUI
Coef1 = []#pre site EUI
Intercept2 = []#pre source EUI
Coef2 = []#pre source EUI
Intercept3 = []#post site EUI
Coef3 = []#post site EUI
Intercept4 = []#post source EUI
Coef4 = []#post source EUI
for row in temp:
    Intercept1.append(float(row[1]))
    Coef1.append(float(row[2])) 
    Intercept2.append(float(row[3]))
    Coef2.append(float(row[4]))    
    Intercept3.append(float(row[5]))
    Coef3.append(float(row[6])) 
    Intercept4.append(float(row[7]))
    Coef4.append(float(row[8])) 

plotDiff(Intercept1,Coef1,Intercept2,Coef2,'pre')
plotDiff(Intercept3,Coef3,Intercept4,Coef4,'post')

