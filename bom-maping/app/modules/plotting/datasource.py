"""
    Author: Saurabh Pandit (s3270950@student.rmit.edu.au)

    This module contains classes to access following datasource from OpenDAP
    servers.
    
        * NetCDF data files
"""

import abc

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
                time_index = 'Default', \
                plot_mask = True
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
        
        
#Implementations

from pydap.client import open_url
import numpy as np
from util.exceptions import NetCDFException

class NetCDFDatasource(IDataSource):
    """
        Author: Saurabh Pandit (s3270950@student.rmit.edu.au)
    
        This class provides some basic functionality for accessing NetCDF data
        from NetCDF files.
        
        url: url of OpenDAP data set
        bbox: TODO
        varname: name of variable/layer/key in string
        time: TODO
        time_index: int value of timestep
        plot_mask: TODO
        

    """
    
    def __init__(self, url, bbox, varname, time, time_index, plot_mask) :
        
        # Pass parameters to the super constructor
        IDataSource.__init__(self, \
                            url, \
                            bbox, \
                            varname, \
                            time, \
                            time_index, \
                            plot_mask \
                            )
        
        try:
            self.dset = open_url(url)
        except :
            raise NetCDFException("Cannot open url")
        
        
        
        
    def get_lats(self):
        """
            Returns all the lattitude values in the data source.
            TODO : raise exception if invalid operation/unexpected error
        """
        return self.dset['lat'][:]
        
        
    def get_lons(self):
        """
            Returns all the longitude values in the data source
            TODO : raise exception if invalid operation/unexpected error
        """
        return self.dset['lon'][:]
        
        
    def get_data(self):
        
        """
            Returns all the data values in the data source
        
        """
        
        if self.time_index == 'Default':
            self.timestep = 0
        else:
            self.timestep = int(self.time_index)
        
        try:
            return self.dset[self.varname][self.timestep,:,:]
        except KeyError as ke:
            
            raise NetCDFException(repr(ke) + " ==> Variable " + self.varname +
                                " does not exist in " +
                                self.dset._id)
            
        
        
    def get_time_units(self):
        
        """
            Returns the unit in which data is represented.
            TODO : raise exception if invalid operation/unexpected error
        """
        
        return self.dset['time'].attributes['units']
        
        
    def get_available_times(self):
        """
            Returns numpy array of availble 'time' variable values in data
            source.
            TODO : raise exception if invalid operation/unexpected error
        """
        
        time_var = self.dset['time']
        return np.array(time_var[:])