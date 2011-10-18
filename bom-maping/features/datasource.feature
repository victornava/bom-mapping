Feature: Datasource
  
  Scenario: error on invalid url
    Given the parameters are set to "default"
    And the value of "source_url" parameter is "invalid_url"
    When I submit the request
    Then it should return a "ServiceException" error with code "DatasourceNotSupported"
    
  Scenario: error on url that's not a pydap server
    Given the parameters are set to "default"
    And the value of "source_url" parameter is "http://example.com"
    When I submit the request
    Then it should return a "ServiceException" error with code "DatasourceNotSupported"
    
  Scenario: error on netcdf file that doesn't exists
    Given the parameters are set to "default"
    And the value of "source_url" parameter is "http://localhost:8001?i_dont_exit.nc"
    When I submit the request
    Then it should return a "ServiceException" error with code "InvalidParameterValue"
      And the message should contain "source_url"
      
  Scenario: error on a layer that doesn't exists in the netcdf file
    Given the parameters are set to "default"
    And the value of "layers" parameter is "undefined"
    When  I submit the request
    Then  it should return a "ServiceException" error with code "LayerNotDefined"
    
  Scenario: can access external data source
    Given the parameters are set to "default"
    And the value of "source_url" parameter is "http://opendap.jpl.nasa.gov/opendap/GeodeticsGravity/tellus/L3/land_mass/netcdf/GRACE.CSR.LAND.RL04.DS.G300KM.nc"
    And the value of "layers" parameter is "lwe_thickness"
    When  I submit the request
    Then the response should be an image
      
  Scenario: can access data source from a local file
    Given the parameters are set to "default"
    And the value of "source_url" parameter is "/Users/vic/dev/bom-mapping/code/bom-maping/pydap-server/data/ocean_latest.nc"
    When  I submit the request
    Then the response should be an image
