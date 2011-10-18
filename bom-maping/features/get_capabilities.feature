Feature: Get capabilities

  Scenario: can get capabilities
		Given the parameters are set to "empty"
			And the value of "request" parameter is "GetCapabilities"
    When I submit the request
    Then the response should be an "xml" document


	Scenario: capabilities has the right tags
		Given the parameters are set to "empty"
			And the value of "request" parameter is "GetCapabilities"
    When I submit the request
    Then the document should have tag "WMS_Capabilities"
			And the document should have tag "Service"
			And the document should have tag "ContactInformation"
			And the document should have tag "Request"
			And the document should have tag "GetMap"
			And the document should have tag "GetCapabilities"
			And the document should have tag "GetFullFigure"
			And the document should have tag "GetLegend"
			And the document should have tag "Exception"
			And the document should have tag "Layer"  
  
  

  
