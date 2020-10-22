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
#regression for one climate
######################################################
def regression(climate):
    
    # get ASHRAE EUI from csv
    with open('./ASHRAEModel_energy_data.csv','r') as f:
        temp = list(csv.reader(f,delimiter=','))
    X_site = []
    X_source = []
    for row in temp:
        if row[1] == climate:
            temp1 = []
            temp2 = []
            temp1.append(float(row[3]))# site EUI
            temp2.append(float(row[4])) #source EUI
            X_site.append(temp1)
            X_source.append(temp2)
    
    # get beQ EUI from csv
    with open('./bEQModel_energy_data.csv','r') as f:
        temp = list(csv.reader(f,delimiter=','))
    Y_site = []
    Y_source = []
    for row in temp:
        if row[1] == climate:
            temp1 = []
            temp2 = []
            temp1.append(float(row[3]))# site EUI
            temp2.append(float(row[4])) #source EUI
            Y_site.append(temp1)
            Y_source.append(temp2)
            

    # calculate adjustment factor       
    linreg1 = LinearRegression()
    model1 = linreg1.fit(X_site,Y_site)
    factor1=linreg1.coef_
    intercept1=linreg1.intercept_    

    linreg2 = LinearRegression()
    model2 = linreg2.fit(X_source,Y_source)
    factor2=linreg2.coef_
    intercept2=linreg2.intercept_

    return model1,model2,factor1,intercept1,factor2,intercept2


    
######################################################
#plot figure
######################################################
def plotDiff(Intercept1,Coef1,Intercept2,Coef2):
    plt.rcParams["font.family"] = "Times New Roman"

    cz = ['1A','2A','2B','3A','3B','3C','4A','4B','4C','5A','5B','6A','6B','7A','8A']

    Y1_model = []# site EUI (model)
    Y1_calc = []# site EUI (calculate)
    Y2_model = []#  source EUI (model)
    Y2_calc =[]#  source EUI (calculate)
     

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

    # get beQe EUI from csv
    with open('./bEQModel_energy_data.csv','r') as f:
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
        
    #draw the line to express Y1_model = Y1_calc
    n1 = 151
    n2 = 401
    
    cent_line1 = range(0,n1)
    cent_line2 = range(0,n2)
    
    #draw the line to express 10% error
    err_1 = []
    for i in range(0,n1):
        err_1.append(0.95*i)

    err_2 = []
    for i in range(0,n2):
        err_2.append(0.95*i)
    
    # plot the figures
    plt.subplot(211)
    plt.scatter(Y1_model,Y1_calc,marker = '.',s = 50,c = 'k')
    plt.plot(cent_line1,cent_line1,'k')
    plt.plot(cent_line1,err_1,'k--')
    plt.plot(err_1,cent_line1,'k--')

    plt.xlabel('Modeled bEQ site EUI'+r'(kBTU/ft$^2$)')
    plt.ylabel('Calculated bEQ site EUI'+'\n'+r'(kBTU/ft$^2$)')
    plt.text(60,110,'Relative Error = 5%',rotation=20)
    plt.text(65,85,'Relative Error = 5%',rotation=19)
    
    plt.xlim([0,150])
    plt.ylim([0,150])
    
    plt.subplot(212)
    plt.scatter(Y2_model,Y2_calc,marker = '.',s = 50,c = 'k')
    plt.plot(cent_line2,cent_line2,'k')
    plt.plot(cent_line2,err_2,'k--')
    plt.plot(err_2,cent_line2,'k--')

    plt.xlabel('Modeled bEQ source EUI '+r'(kBTU/ft$^2$)')
    plt.ylabel('Calculated bEQ source EUI'+'\n'+r'(kBTU/ft$^2$)')
    plt.text(150,300,'Relative Error = 5%',rotation=20)
    plt.text(160,210,'Relative Error = 5%',rotation=19)
    
    plt.xlim([0,400])
    plt.ylim([0,400])
    
    plt.tight_layout() 
    plt.savefig('regression.svg')
    plt.show()

#plotDiff(source_baseline,site_baseline,new_model_data,Coef1,Coef2)

