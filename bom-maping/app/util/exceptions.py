""" Custom Exceptions """

class BBoxException(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return repr(self.message)
        
class NetCDFException(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return repr(self.message)
        
        
################ WMS Exceptions ################

class WMSBaseError(Exception):
    """ Base Class for Exception. Subclass for more easy access """

    def __init__(self,message):
        self.message = message
        self.code = self.__class__.__name__.replace("Error","")
    
    def __str__(self):
        return repr(self.code +": "+ self.message)

        
        
class InvalidFormatError(WMSBaseError):
    """ Exception for representing an invalid image format. """

    
class InvalidCRSError(WMSBaseError):
    """ Exception for representing an invalid CRS """
        
        
class LayerNotDefinedError(WMSBaseError):
    """ Exception for representing and invalid layer """
      
        
class StyleNotDefinedError(WMSBaseError):
    """ Exception for representing an invalid style """
  
        
class MissingDimensionValueError(WMSBaseError):
    """ Excption for representing a missing dimension parameter """
        
        
class InvalidDimensionValueError(WMSBaseError):
    """ Excepton for representing an invalid dimension parameter"""
        
        
class OperationNotSupportedError(WMSBaseError):
    """ Excepton for representiong an invalid operation"""
        
        
########################### Custom errors not in WMS

class MissingParameterError(WMSBaseError):
    """ Exception for missing mandatory parameter"""
