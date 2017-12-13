##############################################
# 照片美化并保存到本地
import imghdr
from os
from routers.basehandler import BaseHandler

from config import IMG_SUPPORTS, DEFAULT_IMG_EXT
from libs import imgBeauty, imgNo


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
            saveStartNo: "001",   // save
        }
        """
        data = self.data
        vBrght = data.get('brightness')
        vCntrst = data.get('contrast')
        if vBrght is None and vCntrst is None:
            return cls.jsonResponse({'msg': 'params error: brightness and contrast both is None', 'status': 1}, 400)
        if not data:
            return cls.jsonResponse({'msg':'empty data', 'status': 1}, 400)
        if not data.get('originAddr'):
            return cls.jsonResponse({'msg': 'no originAddr', 'status': 1}, 400)
        if not data.get('targetAddr'):
            return cls.jsonResponse({'msg': 'no targetAddr', 'status': 1}, 400)
        addr = data['originAddr']
        toAddr = data['targetAddr']
        # start no. for save image name
        saveStartNo = imgNo.DEF_START_IMG_NO
        if data.get('saveStartNo'):
            if imgNo.RE_OBJ_IMG_NO.match(data.get('saveStartNo')):
                saveStartNo = data['saveStartNo']
            else:
                return cls.jsonResponse({'msg': 'Invalid StartNo: %s' % data['saveStartNo'], 'status': 1}, 400)

        if not os.path.exists(addr):
            return cls.jsonResponse({'msg': 'not a valid image file or folder', 'status': 1}, 400)
        if not os.path.isdir(toAddr):
            return cls.jsonResponse({'msg': 'targetAddr must be folder', 'status': 1}, 400)

        imgUrls = []
        svImgExt = None
        if os.path.isfile(addr):
            imgExt = imghdr.what(addr)
            if imgExt not in IMG_SUPPORTS:
                return cls.jsonResponse({'msg': 'only support image formats: %s' % IMG_SUPPORTS, 'status': 1}, 400)
            if not svImgExt:
                svImgExt = DEFAULT_IMG_EXT
            imgUrls.append(addr)
        elif os.path.isdir(addr):
            # find all supported images
            for f in os.listdir(addr):
                fpath = os.path.join(addr, f)
                if os.path.isfile(fpath):
                    imgExt = imghdr.what(fpath)
                    if imgExt in IMG_SUPPORTS:
                        imgUrls.append(fpath)
                        if not svImgExt:
                            svImgExt = DEFAULT_IMG_EXT
        if not imgUrls:
            return cls.jsonResponse({'msg': 'not find images with the path', 'status': 1}, 400)
        if not svImgExt:
            svImgExt = DEFAULT_IMG_EXT
        # generae save names of image
        saveNos = imgNo.geneImgNos(saveStartNo, num=len(imgUrls))
        # process the images
        for img, snm in zip(imgUrls, saveNos):
            # beauty
            imgData = ImageEnhance.Brightness(img)
            if vBrght is not None:
                imgData = imgBeauty.brightnessImage(imgData)
            if vCntrst is not None:
                imgData = imgBeauty.ContrastImage(imgData)
            # save
            svImgPath = os.path.join(toAddr, "%s.%s" % (snm, svImgExt))
            imgData.save(svImgPath)
        return cls.jsonResponse({'status': 0})
