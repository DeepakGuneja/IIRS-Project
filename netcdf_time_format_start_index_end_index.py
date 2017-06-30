########Import the following
import netCDF4
from datetime import datetime

###########

def list_variables(filename):    
    dset = netCDF4.Dataset(filename)
    variables = dset.variables.keys()
    variables = map(lambda x: x.encode('ascii','replace'), variables)
    return variables

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
    
   
def start_index(filename, user_start_date):
    time_format = time_format(filename)
    dset = netCDF4.Dataset(filename)
    times = dset.variables['time']
    jd11 = netCDF4.num2date(times[0],times.units)
    
    date_first = jd11.strftime('%d/%m/%Y')
    
    a = datetime.strptime(user_start_date[0:10], "%d/%m/%Y")
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

    
def last_index(filename, user_end_date):
    time_format = time_format(filename)
    dset = netCDF4.Dataset(filename)
    times = dset.variables['time']
    jd11 = netCDF4.num2date(times[0],times.units)
    
    date_first = jd11.strftime('%d/%m/%Y')
    
    a = datetime.strptime(user_end_date[12:], "%d/%m/%Y")
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





