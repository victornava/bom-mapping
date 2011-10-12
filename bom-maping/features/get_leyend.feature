Feature: Get leyend
  In order to value
  As a role
  I want feature

  Scenario: can get the leyend
    Given the parameters are set to "default"
    And the value of "request" parameter is "GetLegend"
    When I submit the request
    Then the response should be an image
  
  
  
