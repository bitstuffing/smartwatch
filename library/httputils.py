import usocket
import gc

class HttpUtils():

    @staticmethod
    def download_url(url,filename='temp.tmp'):
        headers={}
        headers["User-Agent"]="Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
        HttpUtils.get_url(url=url,headers=headers,download=True,fileName=filename)

    @staticmethod
    def get_url(url, data=None, method='GET',headers={},brute_response=False,download=False,fileName=''):
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
            if not download:
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
            else:
                forigin = s.makefile()
                fdest = open(fileName,"w")
                fdest.write(forigin.read())
                fdest.close()
                forigin.close()
                s.close()
        except OSError:
            s.close()
            pass
        return response
