""" Capabilities Controller

All functionality that has to do with getCapabilities goes into this module.

"""

import config
import util.exceptions as ex


def get_capabilities(params,defaults):
    """ Returns a capabilities dictionary & format """
    cap = CapabilitiesController (params,defaults)
    return cap.get_capabilities()


class CapabilitiesController():
    """ Capabilities Controller

    This class controlls all the get capabilities related functionality.
    Functions are based on the WMS XML Schema.
    Ref: http://schemas.opengis.net/wms/1.3.0/capabilities_1_3_0.xml
    """
    
    def __init__(self, params, defaults):
        """ Constructor

        """

        self.defaults = defaults
        
        # lowercase all the keys/values
        self.params = dict((k.lower(), v.lower()) for k,v in params.items())
        
        if 'format' not in self.params:
            self.params['format'] = defaults['format']
        
        # convert 'text/xml' into 'xml' 
        self.params['format'] = self.params['format'].split('/')[-1]

        # validate verion number & if it's not specified,assign the default value
        if "version" in self.params:
            if self.params['version'] != config.available['version']:
                raise ex.InvalidVersionError(self.params['version'])
        else:
            self.params['version'] = defaults['version']

        # validate service name & if it's not specified,assign the default value
        if "service" in self.params:
            if self.params['service'] != config.available['service']:
                raise ex.InvalidServiceError(self.params['service'])
        else:
            self.params['service'] = defaults['service']

        #TODO : Validating Sequence Parameter


    def get_capabilities(self):
        
        service = self.__get_service()
        capability = self.__get_capability()
        contents = {"service" : service, "capability" : capability}
        return contents, self.params['format']


    def __get_service(self):

        service_basic_info = self.__get_service_basicinfo()
        contact_info = self.__get_service_contactinfo()

        service = service_basic_info
        service['contact_info'] = contact_info
        return service

    def __get_service_basicinfo(self):
        return config.service_basic_info

    def __get_service_contactinfo(self):
        return config.contact_info

    def __get_capability(self):

        request = self.__get_capability_request()
        exception = self.__get_capability_exception()
        layer = self.__get_capability_layer()
        
        capability = { "request": request, "exception" : exception,
                       "layer" : layer}
        return capability

    def __get_capability_request(self):
        # TODO
        return "request details"

    def __get_capability_exception(self):
        return {"formats" : config.available['exception_formats']}
    
    def __get_capability_layer(self):
        # TODO
        return "layer details"
