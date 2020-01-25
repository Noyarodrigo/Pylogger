#generates the html with the values


self.request.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
self.request.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
self.request.send(str.encode('\r\n'))
with open ('index.html','r') as index:
 for l in index:
     self.request.sendall(str.encode(""+l+"", 'iso-8859-1'))

