########################################
##        通用工具
import urllib


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
