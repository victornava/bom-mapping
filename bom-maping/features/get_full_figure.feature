Feature: Get map
  
  Scenario: Returns an image for default parameters 
    Given the parameters are set to "default"
			And the value of "request" parameter is "GetFullFigure"
    When I submit the request
    Then the response should be an image
