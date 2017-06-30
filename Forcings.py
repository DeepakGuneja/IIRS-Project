import netCDF4
from netCDF4 import Dataset
import numpy as np
import time
import os
import math
from datetime import datetime

files = []

def netCDF_file(filename):
    selected_file = []
    selected_file.append(filename)
    return selected_file
##    print "Opened in Forcings %s"%(files[0])

##    print files


def selected_param(selected_file, parameter):
    selected_file.append(parameter)
    return selected_file

def addtoFiles(selected_file):
    files.append(selected_file)

def chgdir(directory):
    os.chdir(directory)

def entered_date(date):
    date = date
##    print date    

def desired_time_format(des_time):
    time_form = int(des_time)
##    print time_form

def choice_for_temp(choice_temp):
    choice = int(choice_temp)
##    print choice

def time_format(filename):
    ''' Time format
        0 - 0,12,0,12...,3,6,9,15,18,21 {skewed 3 hour format}
        1 - 0,12,0,12...,0,12,0,12,0,12 {12 hour format}
        2 - 0,3,6,9,12,15,18,21,0... {3 hour format}
        3 - 0,6,12,18,0... {6 hour format}
        4 - 0,0... {24 hour format}
    '''
    dset = netCDF4.Dataset(filename)
    times = dset.variables['time']
    jd11 = netCDF4.num2date(times[0:10],times.units)
    jd22 = netCDF4.num2date(times[len(times)-10:],times.units)
    time_first = [time.strftime('%H') for time in jd11]
    time_last = [time.strftime('%H') for time in jd22]
    
    if time_first[0] == '00' and time_first[1] == '00':
        return 4
    elif time_first[0] == '00' and time_first[1] == '03':
        return 2
    elif time_first[0] == '00' and time_first[1] == '12':
        if (time_last[0] == '00' and time_last[1] == '12') or (time_last[1] == '00' and time_last[0] == '12') :
            return 1
        else:
            return 0
    elif time_first[0] == '00' and time_first[1] == '06':
        return 3
    
   
def start_index(filename, user_date):
    time_format = time_format(filename)
    dset = netCDF4.Dataset(filename)
    times = dset.variables['time']
    jd11 = netCDF4.num2date(times[0],times.units)
    
    date_first = jd11.strftime('%d/%m/%Y')
    
    a = datetime.strptime(user_date[0:10], "%d/%m/%Y")
    b = datetime.strptime(date_first, "%d/%m/%Y")
    delta = a - b
    ndays = delta.days
    if time_format == 0 or time_format == 1:
        return ndays*2
    elif time_format == 2:
        return ndays*8
    elif time_format == 4:
        return ndays
    elif time_format == 3:
        return ndays*4

    
def last_index(filename, user_date):
    time_format = time_format(filename)
    dset = netCDF4.Dataset(filename)
    times = dset.variables['time']
    jd11 = netCDF4.num2date(times[0],times.units)
    
    date_first = jd11.strftime('%d/%m/%Y')
    
    a = datetime.strptime(user_date[12:], "%d/%m/%Y")
    b = datetime.strptime(date_first, "%d/%m/%Y")
    delta = a - b
    ndays = delta.days
    if time_format == 0 or time_format == 1:
        return ndays*2
    elif time_format == 2:
        return ndays*8
    elif time_format == 4:
        return ndays
    elif time_format == 3:
        return ndays*4
    
def list_variables(filename):    
    dset = Dataset(filename)
    variables = dset.variables.keys()
    variables = map(lambda x: x.encode('ascii','replace'), variables)
    return variables

def getLonLat():
    file1 = Dataset(files[0][0], mode='r')
    list_of_variables = list_variables(files[0][0])
    for i in list_of_variables:
        if 'lat' in i:
            lats_var_name = i
        if 'lon' in i:
            lons_var_name = i
    lons = file1.variables[lons_var_name][:]
    lats = file1.variables[lats_var_name][:]
    file1.close()
    return lons,lats
    
def start_generation():
    number_of_files = len(files)
    lons,lats = getLonLat()
    all_file_data = []
    for i in range(number_of_files):
        ele = []
        file = Dataset(files[i][0], mode='r')
        for param in files[i][1:]:
            ele.append(file.variables[param][:])
        all_file_data.append(ele)
            
