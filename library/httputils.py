import socket

class HttpUtils():

    @staticmethod
    def http_get(url):
        response = ''
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        while True:
            data = s.recv(100)
            if data:
                response+=str(data, 'utf-8', end='')
            else:
                break
        s.close()
        return response
