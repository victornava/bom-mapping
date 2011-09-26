""" Capabilities Controller

All functionality that has to do with getCapabilities goes into this module.
"""
import util.wmsxml as xml
import util.wmsjson as json


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
        
        # considering XML as the default output format(MIME Type)
        self.format = 'text/xml'

        # considering 1.3.0 as the default version
        self.version = '1.3.0'


    def get_capabilities(self):
       
        if "format" in self.params.keys():
            if(self.params['format'] == 'application/json'):
                self.format = 'application/json'

        # TODO - Get Capabilities 
        #( Service, Metadata, Contact .. )
        

        # Test content - Exception
        contents = {'version': self.version , 'lang':'en' ,
                    'exceptions':[{'text':'Test1', 'code':'E1', 'locator':'header'},
                                  {'text':'Test2', 'code':'E2', 'locator':'footer'}]}

        return self.__render_capabilities(contents)


    def __render_capabilities(self,contents): 
        if (self.format == 'application/json'):
            return json.output(contents)
        else:
            return xml.output(contents)

    def __get_service(self):
        # TODO
        pass

    def __get_contact(self):
        # TODO
        pass
