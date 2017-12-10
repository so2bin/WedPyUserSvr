##############################################
# 默认
from routers.basehandler import BaseHandler


class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        request.data = "hello world"
        return cls.jsonResponse(request)

    @classmethod
    def d0Post(self, request):
        pass
