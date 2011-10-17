Feature: Get legend

  Scenario: can get the legend
    Given the parameters are set to "default"
    And the value of "request" parameter is "GetLegend"
    When I submit the request
    Then the response should be an image
  
  
  
