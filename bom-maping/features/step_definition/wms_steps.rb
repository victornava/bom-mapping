begin require 'rspec/expectations'; rescue LoadError; require 'spec/expectations'; end
require 'net/http'
require 'image_size'


Before do
  @base_url = "http://localhost:8007?"
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
    #"color_scale_range" => "-4,4",
    "color_scale_range" => "auto",
    "n_colors" => "10" ,
    "palette" => "jet"
  }
  @url = ""
end

After do 
end

Given /^The parameter (\w+) is missing$/ do |parameter|
  @params = @default_params
  @params.delete(parameter)
end

# Given /^The value of "(.*)" parameter is "(.*)"$/ do |parameter, value|  
Given /^The value of "(.*)" parameter is "(.*)"$/ do |parameter, value|  
  @params = @default_params
  @params[parameter] = value
end

When /^I submit the request$/ do
  # puts make_url(@base_url, @params)
  url = make_url(@base_url, @params)
  puts "\n"+url
  @response = visit url
end

Then /^it should return a "([^"]*)" error with code "([^"]*)"$/ do |error, code|
  # @response['content-type'].should include('text/html')
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

Then /^the "([^"]*)" of the image should be "([^"]*)"$/ do |param, value|
  image_size(@response.body)[param].should == value.to_i
end


# helpers

def visit(url)
  @response = Net::HTTP.get_response(URI.parse(url))
end

# Makes a url string based on the base_url string and a hash with the query parameters
# input:
#  url = http:localhost?
#  params = {a => 1, b => 2}
# out: http:localhost?a=1&b=2
def make_url(base_url, params)
  base_url << params.to_a.reduce([]){|a,kv| a << kv.join("=")}.join("&")
  # base_url << "?" << params.to_a.reduce([]){|a,kv| a << kv.join("=")}.join("&")
end

def image_type(img)
  ImageSize.new(img).get_type.downcase
end

def image_size(img)
  size = ImageSize.new(img).get_size
  {"width" => size[0], "height" => size[1]}
end