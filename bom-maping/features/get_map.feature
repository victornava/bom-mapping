Feature: Get map
  In order to value
  As a role
  I want feature
  
  Scenario: can get an image with default parameters
    Given the parameters are set to "default"
    When I submit the request
    Then the response should be a "png" image
    
  Scenario: can set the size of the image
    Given The value of "width" parameter is "800"
      And The value of "height" parameter is "600"
    When I submit the request
    Then the "width" of the image should be "800"
      And the "height" of the image should be "600"
  

  # Scenario: can get an image with default parameters
  #   Given the parameters are set to "default"
  #   When I submit the request
  #   Then the response should be a "png" image
  
  
  

  
