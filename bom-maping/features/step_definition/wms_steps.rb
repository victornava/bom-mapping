begin require 'rspec/expectations'; rescue LoadError; require 'spec/expectations'; end

Before do
  @base_url = "http://localhost:8007?"
  @url = ""
end

After do
end

Given /^The parameter (\w+) is missing$/ do |parameter|
  @base_url.should_not include(parameter)
end

Given /^The parameter "([^"]*)" is "([^"]*)"$/ do |parameter, value|
  @url == @base_url << "#{parameter}=#{value}"
end

When /^I submit the request$/ do
  @url = @base_url
  @reply = visit @url
end

Then /^it should return a "([^"]*)" error$/ do |error|
  @reply.should include(error)
end  

Then /^the message should contain "?([^"]*)"?$/ do |message|
  @reply.should include(message)
end

# TODO replace with real visit url method
def visit(url)
  `curl -s #{url}`
end

# require 'uri'
# require 'cgi'
# 
# url = "http://localhost:8007?request=GetMap&dap_url=http://blah.com/dap/file.nc"
# uri = URI.parse(url)
# puts CGI.parse(uri.query)