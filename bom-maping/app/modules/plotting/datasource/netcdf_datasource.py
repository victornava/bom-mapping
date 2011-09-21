"""
    Author: Saurabh Pandit (s3270950@student.rmit.edu.au)
    
    This class provides some basic functionality for accessing NetCDF data from
    NetCDF files.
"""

import abc
from i_datasource import IDataSource
from pydap.client import open_url
import numpy as np
from util.exceptions import NetCDFException

class NetCDFDatasource(IDataSource):
        
        
    def __init__(self,url, bbox, varname, time, time_index, plot_mask) :
        
        # Pass parameters to the super constructor
        IDataSource.__init__(self, \
                            url, \
                            bbox, \
                            varname, \
                            time, \
                            time_index,\
                            plot_mask \
                            )
        
        try:
            self.dset = open_url(url)
        except :
            raise NetCDFException("Cannot open url")
        
        self.varname = varname
        print "NetCDFDataSource construct"
        
        
    def get_lats(self):
        """
            Returns all the lattitude values in the data source.
        """
        print "get_lats in NetCDFDataSource"
        return self.dset['lat'][:]
        
        
    def get_lons(self):
        """
            Returns all the longitude values in the data source
        """
        print "get_lons in NetCDFDataSource"
        return self.dset['lon'][:]
        
        
    def get_data(self):
        """
            Returns all the data values in the data source
        """
        print "get_data in NetCDFDataSource"
        
        try:
            return self.dset[self.varname][:]
        except KeyError as ke:
            #raise NetCDFException(repr(ke) + "v")
            
            raise NetCDFException(repr(ke) + " ==> Variable " + self.varname +
                                " does not exist in " +
                                self.dset._id)
            
        
        
    def get_time_units(self):
        """
            Returns the unit in which data is represented.
        """
        print "get_units in NetCDFDataSource"
        return self.dset['time'].attributes['units']
        
        
    def get_available_times(self):
        """
            Returns numpy array of availble 'time' variable values in data
            source.
        """
        print "get_available_times in NetCDFDataSource"
        time_var = self.dset['time']
        return np.array(time_var[:])