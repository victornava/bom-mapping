begin require 'rspec/expectations'; rescue LoadError; require 'spec/expectations'; end
require 'net/http'
require 'image_size'


Before do
  @base_url = "http://localhost:8007?"
  @default_params = {
    "request" => "GetMap",
    "bbox" => "0,-90,360,90",
    "width"=> "300",
    "height"=> "400",
    # "layers"=> "hr24_prcp",
    "layers" => "SSTA",
    "styles" => "contour",
    "crs"=>"EPSG:4283",
    "format"=>"png" ,
    "time"=>"Default" ,
    "time_index"=>"Default" ,
    # "source_url": "http://localhost:8001/atmos_latest.nc",
    "source_url" => "http://localhost:8001/ocean_latest.nc",
    "color_range"=>"-10,10" ,
    "n_color" => "10" ,
    "palette" => "jet"
  }
  @url = ""
end

After do 
end

Given /^The parameter (\w+) is missing$/ do |parameter|
  @base_url.should_not include(parameter)
end

Given /^The value of "(.*)" parameter is "(.*)"$/ do |parameter, value|  
  @params = @default_params
  @params[parameter] = value
end

When /^I submit the request$/ do
  puts make_url(@base_url, @params)
  @response = visit make_url(@base_url, @params)
end

Then /^it should return a "([^"]*)" error with code "([^"]*)"$/ do |error, code|
  @response['content-type'].should include('text/html')
  @response.body.should include(error)
  @response.body.should include(code)
end

Then /^the message should contain "?([^"]*)"?$/ do |message|
  @response.body.should include(message)
end

# get map feature

Given /^the parameters are set to "([^"]*)"$/ do |param|
  @params = @default_params
end

Then /^the response should be a "([^"]*)" image$/ do |type|
  @response['content-type'].should include("image/#{type}")
  image_type(@response.body).should match(type)
end


#helpers

def visit(url)
  @response = Net::HTTP.get_response(URI.parse(url))
end

def make_url(url, params)
  url << params.to_a.reduce([]){|a,kv| a << kv.join("=")}.join("&")
end

def image_type(img)
  ImageSize.new(img).get_type.downcase
end