Feature: Get capabilities

  Scenario: can get capabilities
    Given the parameters are set to "default"
    And the value of "request" parameter is "GetCapabilities"
    When I submit the request
    Then the response should be an "xml" document
  
  
  

  
