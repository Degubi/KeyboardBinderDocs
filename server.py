import http.server

http.server.SimpleHTTPRequestHandler.extensions_map = {
    '.html': 'text/html',
    '.png' : 'image/png',
    '.jpg' : 'image/jpg',
    '.svg' : 'image/svg+xml',
    '.css' : 'text/css',
    '.js'  : 'text/javascript',
    ''     : 'application/octet-stream'
}

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory = 'docs', **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with http.server.HTTPServer(('', 8080), MyHttpRequestHandler) as server:
    server.serve_forever()