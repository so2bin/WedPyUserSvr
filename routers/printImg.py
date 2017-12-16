##############################################
# 打印图片
from .tools.printer import ImgPrinter
from routers.basehandler import BaseHandler


class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        imgName = ImgPrinter.print(request.queryParams['imgUrl'])
        if not imgName:
            request.response = {'status': 1, 'msg': 'Print Error, Maybe Invalid image address'}
        request.response = {'status': 0, 'imgName': imgName}
        return cls.jsonResponse(request)

    @classmethod
    def doPost(self, request):
        pass
