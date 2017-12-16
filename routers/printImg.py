##############################################
# 打印图片
from .tools.printer import ImgPrinter
from routers.basehandler import BaseHandler


class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        """
        @params imgUrl:
        @params tplUrl:  模板地址
        @params rw:  合成时图片保持的宽度比例
        @params rh:  合成时图片保持的高度比例
        @params sx:  合成图片在模板上的起点左边距
        @params sy:  合成图片在模板上的起点上边距
        @params iw:  合成图片在模板上的宽度
        @params ih:  合成图片在模板上的高度
        """
        imgUrl = request.queryParams['imgUrl']
        tplUrl = request.queryParams['tplUrl']
        rw = float(request.queryParams['rw'])
        rh = float(request.queryParams['rh'])
        sx = int(request.queryParams['sx'])
        sy = int(request.queryParams['sy'])
        iw = int(request.queryParams['iw'])
        ih = int(request.queryParams['ih'])
        imgName = ImgPrinter.print(imgUrl, tplUrl, {'h': rh, 'w': rw}, (sx, sy, iw, ih))
        if not imgName:
            request.response = {'status': 1, 'msg': 'Print Error, Maybe Invalid image address'}
        request.response = {'status': 0, 'imgName': imgName}
        return cls.jsonResponse(request)

    @classmethod
    def doPost(self, request):
        pass
