##############################################
# 打印图片
from .tools.printer import ImgPrinter
from routers.basehandler import BaseHandler


def _initPrintParams(param):
    """
    初始化打印参数
    {tmpUrl, tmpW, tmpH, rw, rh, sx, sy, ex, ey, selW, selH, realW, realH}
    """
    newObj = {
        'tmpUrl': param['tmpUrl'], 'tmpW': int(param['tmpW']), 'tmpH': int(param['tmpH']),
        'rw': int(param['rw']), 'rh': int(param['rh']), 'sx': int(param['sx']),'sy': int(param['sy']),
        'ex': int(param['ex']), 'ey': int(param['ey']),
        'selW': int(param['selW']), 'selH': int(param['selH']),
        'realW': int(param['realW']), 'realH': int(param['realH']),
    }
    newObj['selW'] = newObj['selW'] or newObj['tmpW']
    newObj['selH'] = newObj['selH'] or newObj['tmpH']
    return newObj


def _zoomToRealSize(tmp):
    """
    根据实际像素尺寸放大参数
    """
    zoomrate = tmp['realW']/tmp['tmpW']
    tmp['sx'] = round(tmp['sx'] * zoomrate)
    tmp['sy'] = round(tmp['sy'] * zoomrate)
    tmp['ex'] = round(tmp['ex'] * zoomrate)
    tmp['ey'] = round(tmp['ey'] * zoomrate)
    tmp['selW'] = round(tmp['selW'] * zoomrate)
    tmp['selH'] = round(tmp['selH'] * zoomrate)
    return tmp


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
    def doPost(cls, request):
        """
        @params imgUrl:
        @params tplUrl:  模板地址
        @params template:  模板参数
            {lng: {tmpUrl, tmpW, tmpH, rw, rh, sx, sy, ex, ey, selW, selH, realW, realH}, hr: {}}
        """
        imgUrl = request.data['imgUrl']
        tmp = request.data['template']
        lngTmp = tmp['lng']
        hrTmp = tmp['hr']
        newLngTmp = _zoomToRealSize(_initPrintParams(lngTmp))
        newHrTmp = _zoomToRealSize(_initPrintParams(hrTmp))
        imgName = ImgPrinter.print(imgUrl, newLngTmp, newHrTmp)
        if not imgName:
            request.response = {'status': 1, 'msg': 'Print Error, Maybe Invalid image address'}
        request.response = {'status': 0, 'imgName': imgName}
        return cls.jsonResponse(request)
