import usocket
import gc

class HttpUtils():

    @staticmethod
    def get_url(url, data=None, method='GET',headers={},brute_response=False):
        if data is not None:
            method = 'POST'
        response = ''
        path = ''
        try:
            proto, dummy, host, path = url.split('/', 3)
        except ValueError:
            proto, dummy, host = url.split('/', 2)
        port = 80
        if proto == 'https:':
            import ussl
            port = 443
        if ":" in host:
            port = int(host[host.index(":")+1:])
            host = host[:host.index(":")]
        addr = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)[0][-1]
        s = usocket.socket()
        try:
            s.connect(addr)
            if proto == "https:":
                s = ussl.wrap_socket(s)
            s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
            if not "Host" in headers:
                s.write(b"Host: %s\r\n" % host)
            for k in headers:
                s.write(k)
                s.write(b": ")
                s.write(headers[k])
                s.write(b"\r\n")
            if data:
                s.write(b"Content-Length: %d\r\n" % len(data))
            s.write(b"\r\n")
            bruteResponse = s.read()
            s.close()
            #memory issues fix
            #f = s.makefile()
            #bruteResponse = b''
            #line = f.readline()
            #while line:
            #    bruteResponse+=line
            #    line = f.readline()
            #f.close()
            gc.collect()
            bruteResponse = bruteResponse.decode("utf-8")
            if not brute_response and "\r\n\r\n" in bruteResponse:
                response = bruteResponse[bruteResponse.index("\r\n\r\n")+len("\r\n\r\n"):]
            elif not brute_response and "\n\n" in bruteResponse:
                response = bruteResponse[bruteResponse.index("\n\n")+len("\n\n"):]
            else:
                response = bruteResponse
        except OSError:
            s.close()
            pass
        return response
