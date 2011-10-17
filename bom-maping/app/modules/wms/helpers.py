from util.exceptions import InvalidFormatError

def __content_type_format(what, to="content_type"):
	"""
	Convert a content type to a file format (extention) and viceversa
	@what is a format or content type
	@to: is the desired output [content_type or format]
	example:
		__content_type_format("png") -> "image/png"
		__content_type_format("image/png", "content_type") -> "png"
	"""
	
	mapping = {
		"png" : "image/png",
		"svg" : "image/svg+xml",
		"xml" : "text/xml"
		}
		
	if to == "format":
		# swap values and keys
		mapping = dict(zip(mapping.values(), mapping.keys()))
		
	if what in mapping:
		return mapping[what]
	else: 
		raise InvalidFormatError("Don't know how to set "+to+" for: " + str(what));
			

def content_type_for(format):
	"""
	returns the conten type of a given format
	"""
	return __content_type_format(format)
    

def format_for(content_type):
	"""
	returns the format of a given content_type
	"""
	return __content_type_format(content_type, "format")