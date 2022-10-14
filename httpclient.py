#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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
from urllib.parse import urlparse


# from io import BytesIO # my import

# class SocketConverter():
#     def __init__(self, response_bytes):
#         self._file = BytesIO(response_bytes)
#     def makefile(self, *args, **kwargs):
#         return self._file

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

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
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        host = ""
        path = "/"
        port = 80

        parsedUrl = urlparse(url)
        print("parsed:", parsedUrl)

        host = parsedUrl.netloc.split(":")[0] # what if not path?

        if(parsedUrl.path): path = parsedUrl.path
        if(parsedUrl.port): port = parsedUrl.port


        # {colon}{port}
        req = "GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n".format(host=host, path=path, colon=":" if port else "", port=port)
        print("req:", req)

        try:
            self.connect(host, port)
        except:
            print("====== connect failed, throwing 404 ======")
            return HTTPResponse(404, "") # temp, likely want smarter error handling



        self.socket.send(req.encode('utf-8'))
        response = self.socket.recv(4096).decode('utf-8')

        # print("res:", response)

        # not going to be super stable - if there's a \r\n in the body it'll slice that too..
        resArray = response.split("\r\n")

        code = int(resArray[0].split(" ")[1])
        body = resArray[-1]

        print("responding with code:", code)
        print("responding with body:", body)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host = ""
        path = "/"
        port = 80

        parsedUrl = urlparse(url)
        print("parsed:", parsedUrl)

        host = parsedUrl.netloc.split(":")[0] # what if not path?

        if(parsedUrl.path): path = parsedUrl.path
        if(parsedUrl.port): port = parsedUrl.port

        data = ""
        first = True
        for arg in args:
            seperator = "" if first else "&"
            data += (seperator + str(arg) + "=" + str(args[arg]))
            first = False

        data += ("\n\n")

        # print("=========", data)

        content_type = "text/html"
        content_length = str( len( data ) )

        req = "POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: {content_type}\r\nContent-Length: {content_length}\r\n\r\n{data}".format(host=host, path=path, colon=":" if port else "", port=port, content_type=content_type, content_length=content_length, data=data)
        print("req:", req)

        try:
            self.connect(host, port)
        except:
            print("====== connect failed, throwing 404 ======")
            return HTTPResponse(404, "") # temp, likely want smarter error handling



        self.socket.send(req.encode('utf-8'))
        response = self.socket.recv(4096).decode('utf-8')

        # print("res:", response)

        # not going to be super stable - if there's a \r\n in the body it'll slice that too..
        resArray = response.split("\r\n")

        code = int(resArray[0].split(" ")[1])
        body = resArray[-1]

        print("responding with code:", code)
        print("responding with body:", body)

        return HTTPResponse(code, body)

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
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
