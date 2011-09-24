def visit(url)
  `curl -s #{url}`
end