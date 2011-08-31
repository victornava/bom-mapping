import sys

port = 5000
if len(sys.argv)  > 1:
    port = int(sys.argv[1])
if len(sys.argv)  > 2:
    print "arg 2 " + sys.argv[2]

print "using port %i" % port 


print(sys.argv)
