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
    
    def __init__(self,code,message):
        self.code = code
        self.message = message
        
    def __str__(self):
        return repr(self.code +": "+ self.message)

        
        
class InvalidFormatError(WMSBaseError):
    """ Exception for representing an invalid image format. """
    def __init__(self,message):
        WMSBaseError.__init__(self,'InvalidFormat',message)
    

class InvalidCRSError(WMSBaseError):
    """ Exception for representing an invalid CRS """
    def __init__(self,message):
        WMSBaseError.__init__(self,'InvalidCRS',message)
        
        
class LayerNotDefinedError(WMSBaseError):
    """ Exception for representing and invalid layer """
    def __init__(self,message):
        WMSBaseError.__init__(self,'LayerNotDefined',message)
        
        
class StyleNotDefinedError(WMSBaseError):
    """ Exception for representing an invalid style """
    def __init__(self,message):
        WMSBaseError.__init__(self,'StyleNotDefined',message)
        
        
class MissingDimensionValueError(WMSBaseError):
    """ Excption for representing a missing dimension parameter """
    def __init__(self,message):
        WMSBaseError.__init__(self,'MissingDimensionValue',message)
        
        
class InvalidDimensionValueError(WMSBaseError):
    """ Excepton for representing an invalid dimension parameter"""
    def __init__(self,message):
        WMSBaseError.__init__(self,'InvalidDimensionValue',message)
        
        
class OperationNotSupportedError(WMSBaseError):
    """ Excepton for representiong an invalid operation"""
    def __init__(self,message):
        WMSBaseError.__init__(self,'OperationNotSupported',message)