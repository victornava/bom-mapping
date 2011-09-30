import unittest

def ensure(param):
    """docstring for Ensure"""
    return Validator(param)
    
class Validator():
    """docstring for Validator"""
    
    def __init__(self, param):
        self.param = param
        self.exception = ValueError("Invalid: " + str(param))
        self.rule = lambda : True
    
    def is_in(self, iterable):
        self.rule = lambda : self.param in iterable
        return self
            
    def orRaise(self, exception):
        self.exception = exception
        return self
    
    def run(self):
        if not self.rule():
            raise self.exception
        return True

class TestValidator(unittest.TestCase):

    def test_ensure_returns_validator(self):
        self.assertTrue(type(ensure("x")) is Validator)
            
    def test_is_in_with_dict(self):
        validator = ensure("request").is_in({"a":"1", "request":"blah"})
        self.assertTrue(validator.run())
        
    def test_is_in_with_list(self):
        validator = ensure("request").is_in(["a", "b","request"])
        self.assertTrue(validator.run())
        
    def test_is_in_raises_default_exeption(self):
        validator = ensure("request").is_in([])
        self.assertRaises(ValueError, validator.run)
    
    def test_is_in_raises_my_exeption_with_msg(self):
        validator = ensure("request").is_in([]).orRaise(LookupError("the error"))
        self.assertRaisesRegexp(LookupError, "the error", validator.run)
        
    def test_validates_without_rule(self):
        self.assertTrue(ensure("x").run())
            
if __name__ == '__main__':
    unittest.main()
