################ WMS Exceptions ################

class WMSBaseError(Exception):
    """ Base Class for Exception. Subclass for more easy access """

    def __init__(self,message):
        self.message = message
        self.code = self.__class__.__name__.replace("Error","")
    
    def __str__(self):
        return repr(self.code +": "+ self.message)
        
    def data(self):
        return { "code": self.code, "message": self.message }
        
class InvalidFormatError(WMSBaseError):
    """ Exception for representing an invalid image format. """
    
class InvalidCRSError(WMSBaseError):
    """ Exception for representing an invalid CRS """
        
class LayerNotDefinedError(WMSBaseError):
    """ Exception for representing and invalid layer """
        
class StyleNotDefinedError(WMSBaseError):
    """ Exception for representing an invalid style 
    
    Should be raised if there is no such style, e.g. connntooour
    """
        
class MissingDimensionValueError(WMSBaseError):
    """ Excption for representing a missing dimension parameter """
        
class InvalidDimensionValueError(WMSBaseError):
    """ Excepton for representing an invalid dimension parameter"""
        
class CurrentUpdateSequenceError(WMSBaseError):
    """ Excepton raised if the updatesequence parameter is equal to 
        the current value of service metadata update sequence number. 
    """
        
class InvalidUpdateSequenceError(WMSBaseError):
    """ Excepton raised if the updatesequence parameter is greater than 
        the current value of service metadata update sequence number. 
    """
        
class OperationNotSupportedError(WMSBaseError):
    """ Excepton for representiong an invalid operation
    
    Should be raised, if there is no request e.g. GetCrazy
    """
        
########################### Custom errors not in WMS

class MissingParameterError(WMSBaseError):
    """ Exception for missing mandatory parameter"""
    
class InvalidParameterValueError(WMSBaseError):
    """ Exception for invalid values of parameters"""
    
class DatasourceNotSupportedError(WMSBaseError):
    """ Exception for invalid type od datasource """