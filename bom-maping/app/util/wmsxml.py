import sys,os
from genshi.template import TemplateLoader
from pkg_resources import resource_filename

#from xml.dom.minidom import Document,Node
#import ns
# TODO: load other xml cfg file

def output(contents,type='exception'):
    xml = XmlGenerator()
    return xml.output(contents,type)

class XmlGenerator(object):
    """ XML Utiltiy    
    This class is responsible for all xml related functionality.
    """

    def __init__(self):
        """ Constructor """

        # Associate the template directory
        self.template_dirs = os.getcwd().split()
        self.template_dirs.append(resource_filename(__name__, 'templates'))
        self.loader = TemplateLoader(self.template_dirs,auto_reload=True)

        # To create a new XML document, just instantiate a new Document object:
        # self.doc = Document()       


    # TODO : Rename the function
    def make_xml_template(self, contents, type):
        tmpl = self.loader.load('exception_report.xml')
        return str(tmpl.generate(report = contents).render('xml'))


    # Note: This function will be removed later <- TODO
    def make_xml(self):
        # Schema : http://schemas.opengis.net/wms/1.3.0/capabilities_1_3_0.xml

        # Create the <wms> base element
        #TODO : Dictionary/Object has to be used
        '''
        wms = {"root":"WMS_Capabilities"}
        wms_element = self.doc.createElement(wms["root"])
        wms_element.setAttribute("version","1.3.0")
        wms_element.setAttribute("xmlns","http://www.opengis.net/wms")
        wms_element.setAttribute("xmlns:xlink","http://www.w3.org/1999/xlink")
        self.doc.appendChild(wms_element)

        # Service element
        #TODO : Dictionary/Object has to be used
        service_element = self.doc.createElement("Service")
        service_name_element = self.doc.createElement("Name")
        # Give the service_name element some text
        service_name_element_text = self.doc.createTextNode("WMS")
        service_name_element.appendChild(service_name_element_text)
        service_element.appendChild(service_name_element)
        wms_element.appendChild(service_element)

        # Capabilities element
        #TODO : Dictionary/Object has to be used
        capabilities_element = self.doc.createElement("Capability")
        capabilities_request_element = self.doc.createElement("Request")
        capabilities_element.appendChild(capabilities_request_element)
        wms_element.appendChild(capabilities_element)


        # Print our newly created XML
        return self.doc.toprettyxml(indent="  ")
        #return self.doc.toxml()

        # TODO : XML Output using Templates
        # template = xml.templateLoader.load('wms_capabilities_1_3_0.xml')
        '''
        
    def output(self, contents, type):
        #return self.make_xml()
        return self.make_xml_template(contents, type)
