# -*- coding: utf-8 -*-
import socket
import os


def get_response(request):
    request = request.split('\r\n')
    requestHeader = request[0].split(' ')
    if len(requestHeader) < 2:
        return ""
    if requestHeader[0] != 'GET':
        content = "Only GET is allowed here\n"
        return "HTTP/1.1 405 Method Not Allowed\n" \
               "Content-Type: text/plain; encoding=utf8\n" \
               "Content-Length: " + str(len(content)) + "\n" \
               "Connection: closed\n\n" + content
    if requestHeader[2] != 'HTTP/1.1':
        content = "Only HTTP 1.1 is supported\n"
        return "HTTP/1.1 505 HTTP Version Not Supported\n" \
               "Content-Type: text/plain; encoding=utf8\n" \
               "Content-Length: " + str(len(content)) + "\n" \
               "Connection: closed\n\n" + content
    request_dir = requestHeader[1].split('/')
    if request_dir[1] == '':
        content = "Hello mister!\n" \
                  "You are:" + request[5][11:] + "\n"
        return "HTTP/1.1 200 OK\n" \
               "Content-Type: text/plain; encoding=utf8\n" \
               "Content-Length: " + str(len(content)) + "\n" \
               "Connection: closed\n\n" + content
    if request_dir[1] == 'media':
        if len(request_dir) > 2 and request_dir[2] != '':
            if not os.path.isfile('./files/' + request_dir[2]):
                content = "File not found\n"
                return "HTTP/1.1 404 Not found\n" \
                       "Content-Type: text/plain; encoding=utf8\n" \
                       "Content-Length: " + str(len(content)) + "\n" \
                       "Connection: closed\n\n" + content
            f = open('./files/' + request_dir[2], 'r')
            content = ''.join(f.readlines())
            return "HTTP/1.1 200 OK\n" \
                   "Content-Type: text/plain; encoding=utf8\n" \
                   "Content-Length: " + str(len(content)) + "\n" \
                   "Connection: closed\n\n" + content
        files = [f for f in os.listdir('./files') if os.path.isfile('./files/' + f)]
        print files
        content = ' '.join(files)
        return "HTTP/1.1 200 OK\n" \
               "Content-Type: text/plain; encoding=utf8\n" \
               "Content-Length: " + str(len(content)) + "\n" \
               "Connection: closed\n\n" + content
    if request_dir[1] == 'test':
        content = '\n'.join(request)
        return "HTTP/1.1 200 OK\n" \
               "Content-Type: text/plain; encoding=utf8\n" \
               "Content-Length: " + str(len(content)) + "\n" \
               "Connection: closed\n\n" + content
    content = 'Page not found\n'
    return "HTTP/1.1 404 Not found\n" \
           "Content-Type: text/plain; encoding=utf8\n" \
           "Content-Length: " + str(len(content)) + "\n" \
           "Connection: closed\n\n" + content


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  #
server_socket.listen(0)  #

print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  # print IP address and port of client
        request_string = client_socket.recv(2048)  # get client request as a string
        client_socket.send(get_response(request_string))  #
        client_socket.close()
    except KeyboardInterrupt:  # quit on Ctrl^C interrupt
        print 'Stopped'
        server_socket.close()  # close server socket
        exit()
