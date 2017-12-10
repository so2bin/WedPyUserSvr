import urllib
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

import config
import routers
import utils

urls = {
    '^/$': routers.default.HTTPHandler,
    '^/printerLst$': routers.printerList.HTTPHandler,
    '^/printImg$': routers.printImg.HTTPHandler,
    '^/defaultPrinter$': routers.defaultPrinter.HTTPHandler,
    # '^/saveBase64$': routers.
}

# HTTPRequestHandler class
class SimpleHTTPServerRequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        utils.parseQuery(self)
        for url, handler in urls.items():
            urlRe = re.compile(url)
            if urlRe.match(self.path):
                return handler.doGet(self)

    def do_POST(self):
        utils.parseQuery(self)
        for url, handler in urls.items():
            urlRe = re.compile(url)
            if urlRe.match(self.path):
                return handler.doPost(self)

def run():
    print('starting server...')
    server_address = (config.HOST, config.PORT)
    httpd = HTTPServer(server_address, SimpleHTTPServerRequestHandler)
    print('running server on %d...' % config.PORT)
    httpd.serve_forever()

run()
