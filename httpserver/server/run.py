# -*- coding: utf-8 -*-
import socket
import os


def generate_response(code, code_text, content):
    return "HTTP/1.1 " + str(code) + ' ' + code_text + "\n" \
           "Content-Type: text/plain; encoding=utf8\n" \
           "Content-Length: " + str(len(content)) + "\n" \
           "Connection: closed\n\n" + content


def get_response(request):
    request = request.split('\r\n')
    request_header = request[0].split(' ')
    print request
    if len(request_header) < 3:
        return generate_response(400, "Bad Request", "Not enough arguments")
    if request_header[0] != 'GET':
        return generate_response(405, "Method Not Allowed", "Only GET is allowed here\n")
    if request_header[2] != 'HTTP/1.1':
        return generate_response(505, "HTTP Version Not Supported", "Only HTTP 1.1 is supported\n")
    request_dir = request_header[1].split('/')
    if request_dir[1] == '':
        user_agent = next((s for s in request if "User-Agent:" in s), '')
        return generate_response(200, "OK", "Hello mister!\nYou are:" + user_agent[11:] + "\n")
    if request_dir[1] == 'media':
        if len(request_dir) > 2 and request_dir[2] != '':
            if not os.path.isfile('./files/' + request_dir[2]):
                return generate_response(404, "Not found", "File not found\n")
            f = open('./files/' + request_dir[2], 'r')
            return generate_response(200, "OK", ''.join(f.readlines()))
        files = [f for f in os.listdir('./files') if os.path.isfile('./files/' + f)]
        print files
        return generate_response(200, "OK", ' '.join(files))
    if request_dir[1] == 'test':
        return generate_response(200, "OK", '\n'.join(request))
    return generate_response(404, "Not found", "Page not found\n")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # connect socket to port 8000 on localhost
server_socket.listen(0)  # set server to listen on 8000 port

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
