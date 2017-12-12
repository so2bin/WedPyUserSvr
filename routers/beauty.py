##############################################
# 照片美化并保存到本地
import imghdr
from os
from routers.basehandler import BaseHandler

from config import IMG_SUPPORTS
from libs import imgBeauty


class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        request.data = "hello world"
        return cls.jsonResponse(request)

    @classmethod
    def doPost(self, request):
        """
        data: {
            originAddr: "image address on this computer or folder that contains images",
            targetAddr: "folder that used to save the processed images",
            brightness: 1,
            contrast: 1,
            saveStartNum: "001",   // save               ????????????  
        }
        """
        data = self.data
        vBrght = data.get('brightness')
        vCntrst = data.get('contrast')
        if vBrght is None and vCntrst is None:
            return cls.jsonResponse('params error: brightness and contrast both is None')
        if not data:
            return cls.jsonResponse('empty data', 400)
        if not data.get('originAddr'):
            return cls.jsonResponse('no originAddr', 400)
        if not data.get('targetAddr'):
            return cls.jsonResponse('no targetAddr', 400)
        addr = data['originAddr']
        toAddr = data['targetAddr']
        if not os.path.exists(addr):
            return cls.jsonResponse('not a valid image file or folder', 400)
        if not os.path.isdir(toAddr):
            return cls.jsonResponse('targetAddr must be folder', 400)

        imgUrls = []
        if os.path.isfile(addr):
            imgExt = imghdr.what(addr)
            if imgExt not in IMG_SUPPORTS:
                return cls.jsonResponse('only support image formats: %s' % IMG_SUPPORTS)
            imgUrls.append(addr)
        elif os.path.isdir(addr):
            # find all supported images
            for f in os.listdir(addr):
                fpath = os.path.join(addr, f)
                if os.path.isfile(fpath):
                    if imghdr.what(fpath) in IMG_SUPPORTS:
                        imgUrls.append(fpath)
        if not imgUrls:
            return cls.jsonResponse('not find images with the path', 400)
        # process the images
        for img in imgUrls:
            # beauty
            imgData = ImageEnhance.Brightness(img)
            if vBrght is not None:
                imgData = imgBeauty.brightnessImage(imgData)
            if vCntrst is not None:
                imgData = imgBeauty.ContrastImage(imgData)
            # save
