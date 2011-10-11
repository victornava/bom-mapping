Feature: Get map
  In order to value
  As a role
  I want feature
  
  Scenario: Returns an image for default parameters
    Given the parameters are set to "default"
    When I submit the request
    Then the response should be an image
    
  Scenario Outline: Can set the image format
    Given the parameters are set to "default"
      And The value of "format" parameter is "<content_type>"
    When I submit the request
      Then the response should be an image
      And the format of the image should be "<format>"
    
    Examples:
      |content_type | format|
      |image/png    | png   |
      # |image/jpg    | jpg   |
      
  Scenario: Image has the right size
    Given The value of "width" parameter is "800"
      And The value of "height" parameter is "600"
    When I submit the request
    Then the "width" of the image should be "800"
      And the "height" of the image should be "600"

  Scenario Outline: Invalid width or height
    Given The value of "<parameter>" parameter is "<value>"
    When I submit the request
    Then it should return a "ServiceException" error with code "InvalidParameterValue"
  
  Examples:
    | parameter | value |
    | width     |       |
    | width     | x     |
    | width     | 0     |
    | width     | -1    |
    | height    |       |
    | height    | 0     |
    | height    | x     |
    | height    | -1    |
