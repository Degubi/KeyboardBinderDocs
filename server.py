import http.server
import socketserver

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory = 'docs', **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(('', 8080), MyHttpRequestHandler) as httpd:
    httpd.serve_forever()