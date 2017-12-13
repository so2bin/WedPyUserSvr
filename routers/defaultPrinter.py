##############################################
# 默认打印机
from routers.basehandler import BaseHandler
from .tools.printer import Printer

class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        response = Printer.GetDefaultPrinter()
        return cls.jsonResponse(request, response)

    @classmethod
    def doPost(self, request):
        pass
