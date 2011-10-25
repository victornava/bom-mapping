""" Capabilities Controller

All functionality that has to do with getCapabilities goes into
this module.

"""

import config
import util.exceptions as ex


def get_capabilities(params,defaults):
    """ Returns capabilities dictionary & format """
    cap = CapabilitiesController (params,defaults)
    return cap.get_capabilities()


class CapabilitiesController():
    """ Capabilities Controller

    This class controlls all the get capabilities related functionality.
    Functions are based on the WMS XML Schema.
    Ref: http://schemas.opengis.net/wms/1.3.0/capabilities_1_3_0.xml
    Ref: ../templates/capabilities_1_3_0.xml
    """
    
    def __init__(self, params, defaults):
        """ Constructor """

        self.defaults = defaults
        
        # lowercase all the keys
        self.params = dict((k.lower(), v)
                           for k,v in params.items())
        
        if 'format' not in self.params:
            self.params['format'] = defaults['format']

        # convert 'text/xml' into 'xml' 
        self.params['format'] = self.params['format'].split('/')[-1]

        # validate verion number / assign the default value
        if "version" in self.params:
            if self.params['version'] != config.available['version']:
                msg = "version '" +str(self.params['version'])+"' is not supported'"
                raise ex.InvalidVersionError(msg)
        else:
            self.params['version'] = defaults['version']

        # validate service name / assign the default value
        if "service" in self.params:
            if self.params['service'] != config.available['service']:
                msg = "service '" +str(self.params['service'])+"' is not supported'"
                raise ex.InvalidServiceError(msg)
        else:
            self.params['service'] = defaults['service']

    def get_capabilities(self):
        """ Returns capabilities dictionary and output format """

        service = self.__get_service()
        capability = self.__get_capability()
        contents = {"service" : service, "capability" : capability}
        return contents, self.params['format']


    def __get_service(self):
        """
        Returns service metadata info as a dictionary

        """
        
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
        """
        Returns WMS info,
        * Request available,
        * Exception formats
        * layer & style available
        Ref: http://www.opengeospatial.org/standards/wms

        """
        requests = self.__get_capability_request()
        exception = self.__get_capability_exception()
        layers = self.__get_capability_layer()
        
        capability = { "requests": requests,
                       "exception" : exception,
                       "layers" : layers}
        return capability

    def __get_capability_request(self):
        
        requests = {}
        for request in config.available['requests']:
            if request == 'GetCapabilities':
                formats = config.available['capabilities_formats']
            else:
                formats = config.available['image_formats']
                
            request_methods = config.available['request_methods']

            url = config.service_url
            requests.update({request :
                             {"formats" : formats,
                              "request_methods" : request_methods,
                              "url" : url}})
        return requests

    def __get_capability_exception(self):
        return {"formats" : config.available['exception_formats']}
    
    def __get_capability_layer(self):

        #Authority URL - reference to entity id's
        #e.g. auth_url = "http://bom.gov.au/def/ids.."

        '''
        Available Layer(s)..
        For layers and styles relation, ref : openGIS WMS Specification

        '''
        available_layer = {"name" : config.defaults['layers'],
                           "title" : config.defaults['layers'],
                           "crs" : config.defaults['crs'],
                           "bbox" : config.defaults['bbox'].split(","),
                           "styles" : config.available['styles']}

        layers = {"title":config.service_basic_info['title'],
                  "available_layer" : available_layer,
                  "crs":config.defaults['crs']}

        return layers
