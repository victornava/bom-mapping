Feature: wms feature
  
  Scenario Outline: missing parameters
    Given The parameter <parameter> is missing   
    When I submit the request 
    Then it should return a "WMSArgumentError" error
      And the message should contain <message>
      
  Examples:
    | parameter | message                         |
    | request   | request parameter is missing    |
    | crs       | crs parameter is missing        |
    | bbox      | bbox parameter is missing       |
    | width     | width parameter is missing      |
    | height    | height parameter is missing     |
    | format    | format parameter is missing     |