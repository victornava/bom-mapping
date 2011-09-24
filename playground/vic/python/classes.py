class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
        
class A():
    """docstring for A"""
    
    def puts(self, string):
        print string

class B(A):
    """docstring for B"""
    def p(self, string):
        """docstring for p"""
        print string
        
        
A().puts("hello")
B().puts("hello")        
B().p("hello")        