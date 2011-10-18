Feature: WMS Parameter Validation
  In order to ensure WMS compliance
  As a User
  I want to get meaningful xml exceptions when I summit an invalid request

  Scenario: request parameter is not supported
    Given the parameters are set to "default"
    And the value of "request" parameter is "GetCrazy"
    When I submit the request 
    Then it should return a "ServiceException" error with code "OperationNotSupported"
    
  Scenario Outline: bbox parameter doesn't have exactly 4 values
    Given the parameters are set to "default"
    And the value of "bbox" parameter is <value>
    When I submit the request 
    Then it should return a "ServiceException" error with code "MissingDimension"
        # And the message should contain "Missing value in Bounding Box"
        
    Examples:
      | value                 |
      |""                     |
      |"-180.0"               |
      |"-180.0,-90.0,180"     |

  Scenario Outline: bbox parameter has non float values
    Given the parameters are set to "default"
    And the value of "bbox" parameter is <value>
    When I submit the request 
    Then it should return a "ServiceException" error with code "InvalidDimensionValue"
      And the message should contain "Invalid bbox parameter"
      
  Examples:
    | value               |
    |"a,-90.0,180,90"     |
    |"-180.0,a,180,90"    |
    |"-180.0,-90.0,a,90"  |
    |"-180.0,-90.0,180,a" |
 
  Scenario: format parameter is not supported
    Given the parameters are set to "default"
    And the value of "format" parameter is "image/mp3"
    When I submit the request 
    Then it should return a "ServiceException" error with code "InvalidFormat"
      # And the message should contain "Invalid format parameter: image/mp3 format not supported"

  Scenario: styles parameter is invalid
    Given the parameters are set to "default"
    And the value of "styles" parameter is "potato"
    When I submit the request 
    Then it should return a "ServiceException" error with code "StyleNotDefined"
      # And the message should contain "Invalid styles parameter: potato style not supported"
        
  # Scenario: error on invalid format for request
  #   Given the parameters are set to "default"
  #   When event
  #   Then outcome