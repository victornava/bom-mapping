""" Capabilities Controller

All functionality that has to do with getCapabilities goes into this module.
"""

# TODO : Load config files ( address info , abstract, fee etc., )

def get_capabilities(params):
    """ Returns a capabilities in the specified format ( xml/json) """
    cap = CapabilitiesController (params)
    return cap.get_capabilities()


class CapabilitiesController():
    """ Capabilities Controller 
    
    This class controlls all the get capabilities related functionality.
    """
    
    def __init__(self, params):
        """ Constructor """
        self.params = params

        # considering 1.3.0 as the default version
        self.version = '1.3.0'


    def get_capabilities(self):

        # TODO - Get Capabilities 
        #( Service, Metadata, Contact .. )
        
        service = self.__get_service()
        capability = self.__get_capability()
        contents = {"service" : service, "capability" : capability}
        return contents


    def __get_service(self):

        # TODO
        # contact_info = self.__get_service_contactinfo()
        
        # Test content for getCap()
        service = { "name": "WMS", "title": "BOM - Australia" , "abstract" : "Map Overlay Web Service for the Australian Bureu of Meteorology"}
        return service

    def __get_service_contactinfo(self):
        # TODO
        pass

    def __get_capability(self):

        # TODO
        # request = self.__get_capability_request()
        # exception = self.__get_capability_exception()
        # layer = self.__get_capability_layer()
        
        # Test content for getCap()
        capability = { "request": "", "exception:" : "" , "layer" : ""}
        return capability

    def __get_capability_request(self):
        # TODO
        pass

    def __get_capability_exception(self):
        # TODO
        pass
    
    def __get_capability_layer(self):
        # TODO
        pass
