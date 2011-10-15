begin require 'rspec/expectations'; rescue LoadError; require 'spec/expectations'; end
require 'net/http'
require 'image_size'


Before do
  @base_url = "http://localhost:8007"
  @default_params = {
    "request" => "GetMap",
    "bbox" => "-180,-90,180,90",
    "width"=> "400",
    "height"=> "300",
    "layers" => "SSTA",
    "styles" => "contour",
    "crs"=>"EPSG:4283",
    "format"=>"png" ,
    "time"=>"Default" ,
    "time_index"=>"Default" ,
    "source_url" => "http://localhost:8001/ocean_latest.nc",
    "color_scale_range" => "auto",
    "n_colors" => "10" ,
    "palette" => "jet"
  }
end

After do 
end

Given /^the parameter (\w+) is missing$/ do |parameter|
  @params = @default_params
  @params.delete(parameter)
end

Given /^the value of "(.*)" parameter is "(.*)"$/ do |parameter, value|  
  @params[parameter] = value
end

When /^I submit the request$/ do
  url = make_url(@base_url, @params)
  puts "\n"+url
  @response = visit url
end

Then /^it should return a "([^"]*)" error with code "([^"]*)"$/ do |error, code|
  @response.body.should include(error)
  @response.body.should include(code)
end

Then /^the message should contain "?([^"]*)"?$/ do |message|
  @response.body.should include(message)
end

# get map feature
Given /^the parameters are set to "([^"]*)"$/ do |state|
  @params = (state == 'default') ? @default_params : {}
end

Then /^the response should be an image$/ do
  @response['content-type'].should include("image")
  is_image?(@response.body).should == true
end

Then /^the "([^"]*)" of the image should be "([^"]*)"$/ do |param, value|
  image_size(@response.body)[param].should == value.to_i
end

Then /^the format of the image should be "([^"]*)"$/ do |format|
  image_type(@response.body).should match(format)
end

#get_capabilities
Then /^the response should be an "([^"]*)" document$/ do |format|
  @response['content-type'].should include("text/#{format}")
end

  
# helpers
def visit(url)
  @response = Net::HTTP.get_response(URI.parse(url))
end

# Makes a url string based on the base_url string and a hash with the query parameters
# input:
#   base_url = http://localhost
#   params = {a => 1, b => 2}
# output: http:localhost?a=1&b=2
def make_url(base_url, params)
  base_url << "?" << params.to_a.reduce([]){|a,kv| a << kv.join("=")}.join("&")
end

def image_type(img)
  ImageSize.new(img).get_type.downcase
end

def image_size(img)
  i = ImageSize.new(img)
  {"width" => i.get_width, "height" => i.get_height}
end

def is_image?(img)
  ImageSize.new(img).get_height.nil? ? false : true
end