Feature: Datasource
  In order to value
  As a role
  I want feature
  
  Scenario: error on invalid url
    Given The value of "source_url" parameter is "invalid_url"
    When I submit the request
    Then it should return a "ServiceException" error with code "DatasourceNotSupported"
    
  Scenario: error on url that's not a pydap server
    Given The value of "source_url" parameter is "http://example.com"
    When I submit the request
    Then it should return a "ServiceException" error with code "DatasourceNotSupported"
    
  Scenario: error on netcdf file that doesn't exists
    Given The value of "source_url" parameter is "http://localhost:8001?i_dont_exit.nc"
    When I submit the request
    Then it should return a "ServiceException" error with code "InvalidParameterValue"
      And the message should contain "source_url"
      
  Scenario: error on a layer that doesn't exists in the netcdf file
    Given The value of "layers" parameter is "undefined"
    When I submit the request
    Then it should return a "ServiceException" error with code "LayerNotDefined"
    

    
  



  
