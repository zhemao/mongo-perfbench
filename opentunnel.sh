#!/bin/sh

# Open a local tunnel on the database server. 
# Forward port 27017 on the remote server to 27018 on localhost.
# takes the hostname of the remote server as an argument

ssh -fN -L 27018:localhost:27017 $1
