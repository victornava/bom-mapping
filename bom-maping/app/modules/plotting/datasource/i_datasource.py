"""
    Author: Saurabh Pandit (s3270950@student.rmit.edu.au)

    This is the interface to access following datasource from OpenDAP servers.
        
        *NetCDF data files
"""

import abc

class IDataSource(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(self,url, bbox, varname, time, time_index, plot_mask) :
        self.url = url
        self.bbox = bbox
        self.time = time
        self.time_index = time_index
        self.plot_mask = plot_mask
        print "IDataSource construct"
    
    @abc.abstractmethod
    def get_lats(self):
        """
            Returns all the lattitude values in the data source.
        """
        print "get_lats in IDataSource"
    
    @abc.abstractmethod
    def get_lons(self):
        """
            Returns all the longitude values in the data source
        """
        print "get_lons in IDataSource"
    
    @abc.abstractmethod
    def get_data(self):
        """
            Returns all the data values in the data source
        """
        print "get_data in IDataSource"
        
    @abc.abstractmethod
    def get_time_units(self):
        """
            Returns the unit in which data is represented.
        """
        print "get_units in IDataSource"
        
    @abc.abstractmethod
    def get_available_times(self):
        """
            Returns the numpy array of 'time' variable in the data source
        """
        print "get_available_times in IDataSource"