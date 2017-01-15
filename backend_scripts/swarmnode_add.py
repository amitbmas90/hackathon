from flask import Flask, request
import time
import commands
app=Flask("Hostname Allocator")
@app.route("/add")
def increment_node():
    output = ""
    number = request.args['number']
    service = request.args['service']
    command = "docker service scale " +service+"="+number
    print command
    output=commands.getoutput(command)
    return output 
    
@app.route("/numberofcontainers")
def counter():
   service = request.args['service']
   command = "docker service ps "+service + "|"+ "grep -i 'Running'" + "|" + "wc -l"
   return commands.getoutput(command)   


if __name__ == "__main__":
    print " Started\n"
    app.run(host='0.0.0.0',port=9001,debug=True)
