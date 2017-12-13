########################################
##        通用工具
import urllib
import json
import cgi


def parseQuery(self):
    if '?' in self.path:
        paths = self.path.split('?',1)
        self.path = paths[0]
        qrystr = paths[1]
        self.queryString = urllib.parse.unquote(qrystr)
        self.queryParams = urllib.parse.parse_qs(self.queryString)
        self.queryParams = {key: val[0] for key, val in self.queryParams.items()}

    else:
        self.queryString = ""
        self.queryParams = {}

def parsePost(self):
    """
    only support json data
    """
    ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
    if ctype == 'application/json':
        length = int(self.headers['content-length'])
        self.data = json.loads(self.rfile.read(length))
    else:
        self.send_error(415, 'only support json data')
        return
