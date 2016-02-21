import socket
import thread
import subprocess
import sys
import signal
import urllib # Used for decoding special charactes (spaces, commas and UTF-8)

CRLF = '\r\n\r\n'
charset = 'utf8'

def usage():
        print 'Usage: python myHttpServer.py <port-number>'

def sendHttpResponse(clientHandler, statusLine, messageBody):
        '''
        statusLine and messageBody formate obtained from RFC2616
        https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html#sec6       
        '''
        clientHandler.send('HTTP/1.1 ' + statusLine + '\nContent-Type: text/html; charset=' + charset + CRLF + messageBody)
        clientHandler.close()

def extractCommand(msg):
        '''
        Request is contained in the form as mentioned in RFC2616
        https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5
        -----------------------------------------------------------
        Eg.
        GET /exec/ls HTTP/1.1
        Host: 127.0.1.1:6523
        Connection: keep-alive
        Cache-Control: max-age=0
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36
        Accept-Encoding: gzip, deflate, sdch
        Accept-Language: en-US,en;q=0.8,en-AU;q=0.6,hi;q=0.4
        ------------------------------------------------------------
        '''
        command = msg.split(CRLF)[0].split('/exec/')[1].split(' HTTP/1.1')[0]
        command = urllib.unquote(command).decode(charset)
        return command.strip()

def clientThread(clientHandler):
         msg = clientHandler.recv(1024)
         if 'exec/' in msg:
                cmd = extractCommand(msg)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                (stdout, stderr) = p.communicate()
                try:
                        p.kill()
                except:
                        print('Process stopped')
                sendHttpResponse(clientHandler, "200 OK", stdout+stderr)
         else:
                with open('pageNotFound.html', 'r') as myfile:
                        message = myfile.read().replace('\n', '')
                sendHttpResponse(clientHandler, "404 Not Found", message)

if __name__ == "__main__":
        if len(sys.argv) < 2:
                usage()
                sys.exit(1)
        else:
                try:
                        port = int(sys.argv[1])
                except ValueError:
                        print '<port-number> is not an integer'
                        usage()
                        sys.exit(1)
        try:
                s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

                #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((socket.gethostname(), port))
                s.listen(5)
                print 'Listening on', port, '. . .'

        except socket.error, e:
                print "error"
                #print 'Failed when creating socket: [' + str(e[0]) + ', ' + e[1] + ']'
                sys.exit(1)

        while True:
                try:
                        s.listen(2)
                        (clientHandler, addr) = s.accept()
                        thread.start_new_thread(clientThread, (clientHandler, ))               
                except Exception as e:
                        print e
                        sys.exit(1)

# Code to handle system kill (Ctrl+C)
# http://www.linuxjournal.com/article/3946
def signal_handler(signal, frame):
        try:
                s.shutdown(socket.SHUT_RDWR)
                sys.exit(1)
        except:
                sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)
