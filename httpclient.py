    #!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle, Christian Jukna
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse  import urlparse
from urllib import urlencode

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    # def get_host_port(self,url):
    #     return url.port

    # def get_host(self,url):
    #     return url.hostname

    # def get_headers(self,data):
    #     return None

    def connect(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 80 if port == None else port))
        return s

    def get_code(self, data):
        return (int)((((data.split("\n"))[0]).split(" "))[1])

    def get_body(self, data):
        return (data.split("\r\n\r\n",1))[1]

    def parse_url(self,url):
        return urlparse(url)

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        p = self.parse_url(url)
        s = self.connect(p.hostname, p.port)
        r = "GET "+ (p.path if p.path != "" else "/") + " HTTP/1.0\r\nHost: " 
        r += (p.hostname if p.port is None else (p.hostname + ":" + str(p.port))) +"\r\n\r\n"
        
        try:
            s.sendall(r)
            d = self.recvall(s)
        finally:
            s.close()
        
        code = self.get_code(d)
        body = self.get_body(d)
        print body
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        p = self.parse_url(url)
        s = self.connect(p.hostname, p.port)
        r = "POST "+ (p.path if p.path != "" else "/") + " HTTP/1.0\r\nHost: "
        r += (p.hostname if p.port is None else (p.hostname + ":" + str(p.port))) +"\r\n"
        r += "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: "
        r += (str(len(urlencode(args))) +"\r\n\r\n" + urlencode(args)) if args != None else ("0\r\n\r\n")
        
        try:
            s.sendall(r)
            d = self.recvall(s)
        finally:
            s.close()

        code = self.get_code(d)
        body = self.get_body(d)
        print body
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( command, sys.argv[1] )    
