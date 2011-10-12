
from netCDF4 import Dataset

#create file
rootgrp = Dataset('test.nc', 'w', format='NETCDF4')
print rootgrp.file_format
rootgrp.close()

#groups in netCDF file
rootgrp = Dataset('test.nc', 'a')
fcstgrp = rootgrp.createGroup('forecasts')
analgrp = rootgrp.createGroup('analyses')
print rootgrp.groups

fcstgrp1 = fcstgrp.createGroup('model1')
fcstgrp2 = fcstgrp.createGroup('model2')

def walktree(top):
        values = top.groups.values()
        yield values
        for value in top.groups.values():
                for children in walktree(value):
                        yield children

for children in walktree(rootgrp):
        for child in children:
                print child
#Dimensions in netCDF file
level = rootgrp.createDimension('level', None)
time = rootgrp.createDimension('time', None)
lat = rootgrp.createDimension('lat', 73)
lon = rootgrp.createDimension('lon', 144)
print rootgrp.dimensions

#printing dimensions
for dimobj in rootgrp.dimensions.values():
        print dimobj


#Variables in netCDF file
times = rootgrp.createVariable('time', 'f8', ('time',))
levels = rootgrp.createVariable('level', 'i4', ('level',))
latitudes = rootgrp.createVariable('latitude', 'f4', ('lat',))
longitudes = rootgrp.createVariable('longitude', 'f4', ('lon',))
temp = rootgrp.createVariable('temp','f4',('time','level','lat','lon',))

#Attributes in a netCDF file
import time
rootgrp.description = 'bogus example script'
rootgrp.history = 'Created ' + time.ctime(time.time())
rootgrp.source = 'netCDF4 python module tutorial'
latitudes.units = 'degrees north'
longitudes.units = 'degrees east'
levels.units = 'hPa'
temp.units = 'K'
times.units = 'hours since 0001-01-01 00:00:00.0'
times.calendar = 'gregorian'

for name in rootgrp.ncattrs():
    print 'Global attr', name, '=',getattr(rootgrp,name)
    
    
#Writing data to and retrieving data from a netCDF variable
import numpy

lats = numpy.arange(-90, 91, 2.5)
lons = numpy.arange(-180, 180, 2.5)

latitudes[:] = lats
longitudes[:] = lons
print 'latitudes =\n',latitudes[:]
print 'longitudes =\n',longitudes[:]

nlats = len(rootgrp.dimensions['lat'])
nlons = len(rootgrp.dimensions['lon'])
print 'temp shape before adding data = ',temp.shape

#Adding data
from numpy.random import uniform
temp[0:5,0:10,:,:] = uniform(size=(5,10,nlats,nlons))
print 'temp shape after adding data = ',temp.shape

# levels have grown, but no values yet assigned.
print 'levels shape after adding pressure data = ',levels.shape

# now, assign data to levels dimension variable.
levels[:] =  [1000.,850.,700.,500.,300.,250.,200.,150.,100.,50.]

# fill in times.
from datetime import datetime, timedelta
from netCDF4 import num2date, date2num

dates = [datetime(2001,3,1)+n*timedelta(hours=12) for n in range(temp.shape[0])]
times[:] = date2num(dates,units=times.units,calendar=times.calendar)
print 'time values (in units %s): ' % times.units+'\n',times[:]

dates = num2date(times[:],units=times.units,calendar=times.calendar)
print 'dates corresponding to time values:\n',dates