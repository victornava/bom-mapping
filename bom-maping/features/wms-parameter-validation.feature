Feature: WMS Parameter Validation
  In order to ensure WMS compliance
  As a User
  I want to have parameter validation
  
  Scenario Outline: Missing parameters
    Given The parameter <parameter> is missing   
    When I submit the request 
    Then it should return a "WMSArgumentError" error
      And the message should contain <message>
      
  Examples:
    | parameter | message                         |
    | request   | request parameter is missing    |
    | bbox      | bbox parameter is missing       |
    | crs       | crs parameter is missing        |
    | width     | width parameter is missing      |
    | height    | height parameter is missing     |
    | format    | format parameter is missing     |
    | version   | version parameter is missing    |
    | layers    | layers parameter is missing     |
    | styles    | styles parameter is missing     |
    

  Scenario: request parameter is not GetMap or GetFeature
    Given The parameter "request" is "GetCrazy"
    When I submit the request 
    Then it should return a "WMSError" error
      And the message should contain "Operation not supported"
      
  Scenario Outline: bbox parameter has missing values
    Given The parameter "bbox" is <value>
    When I submit the request 
    Then it should return a "WMSArgumentError" error
      And the message should contain "ilegal bbox parameter: bbox shuold have 4 values"
      
  Examples:
    | value                   |
    |"-180"                   |
    |"-180,-90,180"           |
    |"-180,-90,180,"          |
    |"-180,-90,180,-180,100"  |
    
  Scenario Outline: bbox parameter has non integer values
    Given The parameter "bbox" is <value>
    When I submit the request 
    Then it should return a "WMSArgumentError" error
      And the message should contain "ilegal bbox parameter: all values should be integers"
      
  Examples:
    | value           |
    |"a,-90,180,90"   |
    |"-180,a,180,90"  |
    |"-180,-90,a,90"  |
    |"-180,-90,180,a" |
    
  # Scenario Outline: bbox parameter has incorrect values
  #   Given The parameter "bbox" is <value>
  #   When I submit the request 
  #   Then it should return a "WMSArgumentError" error
  #     And the message should contain "ilegal bbox parameter: some values are missing"