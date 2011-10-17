Feature: Get capabilities

  Scenario: can get capabilities
		Given the parameters are set to "empty"
			And the value of "request" parameter is "GetCapabilities"
    When I submit the request
    Then the response should be an "xml" document


	Scenario: capabilities has the right element
		Given the parameters are set to "empty"
			And the value of "request" parameter is "GetCapabilities"
    When I submit the request
    Then the document should have tag "WMS_Capabilities"
			And the document should have tag "Service"
  
  
  

  
