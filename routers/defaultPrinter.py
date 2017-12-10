##############################################
# 默认打印机
from routers.basehandler import BaseHandler
from .tools.printer import Printer

class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        request.data = Printer.GetDefaultPrinter()
        return cls.jsonResponse(request)

    @classmethod
    def d0Post(self, request):
        pass
