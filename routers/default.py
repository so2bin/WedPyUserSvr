##############################################
# 默认
from routers.basehandler import BaseHandler


class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        response = "hello world"
        return cls.jsonResponse(request, response)

    @classmethod
    def doPost(cls, request):
        response = "hello world"
        return cls.jsonResponse(request, response)
