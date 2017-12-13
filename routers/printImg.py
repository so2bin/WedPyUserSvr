##############################################
# 打印图片
from .tools.printer import ImgPrinter
from routers.basehandler import BaseHandler


class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        ImgPrinter.print(request.queryParams['imgUrl'])
        request.response = {'status': 0}
        return cls.jsonResponse(request)

    @classmethod
    def doPost(self, request):
        pass
