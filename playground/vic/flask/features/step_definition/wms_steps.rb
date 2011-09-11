begin require 'rspec/expectations'; rescue LoadError; require 'spec/expectations'; end

Before do
  @base_url = "http://localhost:8007"
  @url = ""
end

After do
end

Given /^The parameter (\w+) is missing$/ do |parameter|
  @base_url.should_not include(parameter)
end

When /^I submit the request$/ do
  @url = @base_url
  @reply = visit @url
end

Then /^it should return a "([^"]*)" error$/ do |error|
  @reply.should include(error)
end  

Then /^the message should contain ([^"]*)$/ do |message|
  @reply.should include(message)
  # pending # express the regexp above with the code you wish you had
end

# TODO replace with real visit url method
def visit(url)
  # return [ "WMSArgumentError" , "request parameter is missing", "crs parameter is missing"].join("\n")
  return ""
end