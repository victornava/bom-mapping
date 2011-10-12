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

