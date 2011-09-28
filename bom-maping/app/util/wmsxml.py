import sys,os
#from jinja2 import Template, Context, FileSystemLoader
from jinja2 import *
#from genshi.template import TemplateLoader
#from pkg_resources import resource_filename

#from xml.dom.minidom import Document,Node
#import ns
# TODO: load other xml cfg file

def output(contents,type='exception'):
    out = OutputGenerator()
    return out.generate_output(contents,type)

class OutputGenerator(object):
    """ XML Utiltiy    
    This class is responsible for all xml related functionality.
    """

    def __init__(self):
        """ Constructor """

        # Associate the template directory
        #self.template_dirs = os.getcwd().split()
        #self.template_dirs.append(resource_filename(__name__, 'templates'))
        #self.loader = TemplateLoader(self.template_dirs,auto_reload=True)

        # To create a new XML document, just instantiate a new Document object:
        # self.doc = Document()       


    # TODO : Rename the function
    def make_xml(self, contents, type):
        #tmpl = self.loader.load('exception_report.xml')
        #return str(tmpl.generate(report = contents).render('xml'))
        pass

        
    def generate_output(self, contents, type):
        #return self.make_xml()
        return self.make_xml(contents, type)
