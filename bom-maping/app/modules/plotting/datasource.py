"""
    Author: Saurabh Pandit (s3270950@student.rmit.edu.au)

    This module contains classes to access following datasource from OpenDAP
    servers.
    
        * NetCDF data files
"""

import abc
from modules.plotting.commons import BBox

class IDataSource(object):
    """
        Author: Saurabh Pandit (s3270950@student.rmit.edu.au)

        This is the interface to access following datasource from OpenDAP
        servers
        
        *NetCDF data files
    """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(self, \
                url, \
                bbox, \
                varname, \
                time, \
                time_index, \
                plot_mask
                ) :
        self.url = url
        self.bbox = bbox
        self.varname = varname
        self.time = time
        self.time_index = time_index
        self.plot_mask = plot_mask
        
        #=======#
        self.timestep = 0
        
    
    @abc.abstractmethod
    def get_lats(self):
        """
            Returns all the lattitude values in the data source.
        """
        pass
    
    @abc.abstractmethod
    def get_lons(self):
        """
            Returns all the longitude values in the data source
        """
        pass
    
    @abc.abstractmethod
    def get_data(self):
        """
            Returns all the data values in the data source
        """
        pass
    
    @abc.abstractmethod
    def get_time_units(self):
        """
            Returns the unit in which data is represented.
        """
        pass
    
    @abc.abstractmethod
    def get_available_times(self):
        """
            Returns the numpy array of 'time' variable in the data source
        """
        pass
    
    @abc.abstractmethod
    def get_var_unit(self):
        """
            Returns the unit of variable in string
        """
        pass
    
    @abc.abstractmethod
    def get_init_date(self):
        """
            Returns the data of layer init_date
        """
        pass
    
    @abc.abstractmethod
    def get_time_label(self):
        """
            Returns the value of time_label for given timestep
        """
        pass
    
    
#Implementations

from pydap.client import open_url
import numpy as np
import util.exceptions as ex

class NetCDFDatasource(IDataSource):
    """
        Author: Saurabh Pandit (s3270950@student.rmit.edu.au)
    
        This class provides some basic functionality for accessing NetCDF data
        from NetCDF files.
        
        url: url of OpenDAP data set
        bbox: commons.bbox object
        varname: name of variable/layer/key in string
        time: TODO
        time_index: int value of timestep or 'Default'
        plot_mask: boolean value of 
        

    """
    
    def __init__(self, \
                url, \
                bbox, \
                varname, \
                time = 'Default', \
                time_index = 'Default', \
                plot_mask = True
                ) :
        
        # Pass parameters to the super constructor
        IDataSource.__init__(self, \
                            url, \
                            bbox, \
                            varname, \
                            time, \
                            time_index, \
                            plot_mask \
                            )
        
        #self.bbox.display()
        try:
            self.dset = open_url(url)
        except Exception,e:
            raise ex.InvalidParameterValueError(repr(e))
        
        if self.time_index == 'Default':
            self.timestep = 0
        else:
            self.timestep = int(self.time_index)
        
        
    def get_lats(self):
        """
            Returns all the lattitude values in the data source.
            TODO : raise exception if invalid operation/unexpected error
        """
        #return self.dset['lat'][self.bbox.lat_min:self.bbox.lat_max]
        indices = (self.dset['lat'][:] >= self.bbox.lat_min) & \
                  (self.dset['lat'][:] <= self.bbox.lat_max)
        
        lat_min_index = np.where(indices)[0].min()
        lat_max_index = np.where(indices)[0].max()
        return self.dset['lat'][lat_min_index:lat_max_index + 1]
        
        
    def get_lons(self):
        """
            Returns all the longitude values in the data source
            TODO : raise exception if invalid operation/unexpected error
        """
        #return self.dset['lon'][self.bbox.lon_min:self.bbox.lon_max]
        
        indices = (self.dset['lon'][:] >= self.bbox.lon_min) & \
                  (self.dset['lon'][:] <= self.bbox.lon_max)
        
        lon_min_index = np.where(indices)[0].min()
        lon_max_index = np.where(indices)[0].max()
        return self.dset['lon'][lon_min_index:lon_max_index + 1]
        
        
    def __do_masking(self, var):
        """
            Masks the layer/variable data with masking data depending upon the
            plot_mask parameter.
        """
        
        if 'mask' not in self.dset.keys() or self.plot_mask == False:
            varm = np.ma.masked_array(var, mask=np.isinf(var))
        elif 'mask' in self.dset.keys() and self.plot_mask == True:
            #finding lattitude indices
            indices = (self.dset['mask']['lat'][:] >= \
                            self.bbox.lat_min) & \
                      (self.dset['mask']['lat'][:] <= \
                            self.bbox.lat_max)
            
            lat_min_index = np.where(indices)[0].min()
            lat_max_index = np.where(indices)[0].max()
            
            #finding longitude indices
            indices = (self.dset['mask']['lon'][:] >= \
                            self.bbox.lon_min) & \
                      (self.dset['mask']['lon'][:] <= \
                            self.bbox.lon_max)
            
            lon_min_index = np.where(indices)[0].min()
            lon_max_index = np.where(indices)[0].max()
            
            maskvar = self.dset['mask'][self.timestep, \
                                        lat_min_index:lat_max_index + 1, \
                                        lon_min_index:lon_max_index + 1]
            varm = np.ma.masked_array(var, mask=maskvar)
            mask = varm.mask
        
        return varm
        
    def get_data(self):
        """
            Returns all the data values in the data source
        """
        #finding lattitude indices
        indices = (self.dset[self.varname]['lat'][:] >= \
                        self.bbox.lat_min) & \
                  (self.dset[self.varname]['lat'][:] <= \
                        self.bbox.lat_max)
        
        lat_min_index = np.where(indices)[0].min()
        lat_max_index = np.where(indices)[0].max()
        
        #finding longitude indices
        indices = (self.dset[self.varname]['lon'][:] >= \
                        self.bbox.lon_min) & \
                  (self.dset[self.varname]['lon'][:] <= \
                        self.bbox.lon_max)
            
        lon_min_index = np.where(indices)[0].min()
        lon_max_index = np.where(indices)[0].max()
        
        try:
            var = self.dset[self.varname][self.timestep, \
                                          lat_min_index:lat_max_index + 1, \
                                          lon_min_index:lon_max_index + 1]
        except KeyError as ke:
            raise ex.LayerNotDefined(self.varname + " in " + self.dset._id)
        #Masking
        varm = self.__do_masking(var)
        
        return varm
        
        
    def get_time_units(self):
        
        """
            Returns the unit in which data is represented.
        """
        try:
            time_units = self.dset['time'].attributes['units']
        except KeyError,e:
            raise ex.LayerNotDefined(repr(e))
        return time_units
        
        
    def get_available_times(self):
        """
            Returns numpy array of availble 'time' variable values in data
            source.
        """
        try:
            time_var = self.dset['time']
        except Exception,e:
            raise ex.LayerNotDefined("time")
            
        return np.array(time_var[:])
        
    def get_var_unit(self):
        """
            Returns the unit of variable in string
        """
        
        try:
            var_units = self.dset[self.varname].attributes['units']
        except:
            var_units = ''
        
        return var_units
        
        
    def get_init_date(self):
        """
            Returns the data of layer init_date
        """
        if 'init_date' in self.dset.keys():
            return self.dset['init_date']
        
        
    def get_time_label(self):
        """
            Returns the value of time_label for given timestep
        """
        if 'time_label' in self.dset.keys():
            return self.dset['time_label'][self.timestep]