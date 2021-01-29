#  coding: utf-8
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print("Got a request of: %s\n" % self.data)

        temp = [i.strip() for i in self.data.splitlines()]

        if -1 == temp[0].find(b'HTTP'):
            self.request.sendall(
                bytearray("HTTP/1.1 400 BAD_REQUEST\r\n", 'utf-8'))

        # Figure out our request method, path, and which version of HTTP we're using
        method, path, protocol = [i.strip().decode("utf-8")
                                  for i in temp[0].split()]

        # Create the headers, but only if we have a GET reqeust
        if 'GET' != method:
            self.request.sendall(
                bytearray("HTTP/1.1 405 METHOD_NOT_ALLOWED\r\n", 'utf-8'))

        # Checking the path file type
        file_type = path[path.find('.')+1:]

        # Raising a 404 response code if file type is not HTML or CSS
        # try:
        #     if file_type != 'html' and file_type != 'css':
        #         self.request.sendall(
        #             bytearray("HTTP/1.1 404 FILE_NOT_FOUND\r\n", 'utf-8'))
        #         print("I'm in!!!!")
        # except:
        #     pass

        # Correcting path format
        path = "." + path

        if not os.path.isfile(path):
            self.request.sendall(
                bytearray("HTTP/1.1 404 FILE_NOT_FOUND\r\n", 'utf-8'))

        self.request.sendall(bytearray('Content-Type: text/html\n', 'utf-8'))

        self.request.sendall(
            bytearray("HTTP/1.1 " + open(path, "r").read() + "\r\n", 'utf-8'))

        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n", 'utf-8'))
        self.request.sendall(bytearray('Content-Type: text/html\r\n', 'utf-8'))
        self.request.send(bytearray('\n', 'utf-8'))
        self.request.sendall(bytearray(""+l+"", 'utf-8'))

        # self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n", 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
