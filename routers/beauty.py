##############################################
# 照片美化并保存到本地
import imghdr
import os
import shutil
from routers.basehandler import BaseHandler
from PIL import ImageEnhance, Image

from config import IMG_SUPPORTS, DEFAULT_IMG_EXT
from libs import imgBeauty, imgNo


class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        request.response = "helloworld"
        return cls.jsonResponse(request)

    @classmethod
    def doPost(cls, request):
        """
        data: {
            originAddr: "image address on this computer or folder that contains images",
            targetAddr: "folder that used to save the processed images",
            brightness: 1,
            contrast: 1,
            saveStartNo: "001",   // save
        }
        """
        data = request.data
        vBrght = data.get('brightness')
        vCntrst = data.get('contrast')
        if vBrght is None and vCntrst is None:
            return cls.jsonResponse(request, {'msg': 'params error: brightness and contrast both is None', 'status': 1})
        if not data:
            return cls.jsonResponse(request, {'msg':'empty data', 'status': 1})
        if not data.get('originAddr'):
            return cls.jsonResponse(request, {'msg': 'no originAddr', 'status': 1})
        if not data.get('targetAddr'):
            return cls.jsonResponse(request, {'msg': 'no targetAddr', 'status': 1})
        if not data.get('moveToAddr'):
            return cls.jsonResponse(request, {'msg': 'no moveToAddr', 'status': 1})
        addr = data['originAddr']
        toAddr = data['targetAddr']
        moveAddr = data['moveToAddr']
        # start no. for save image name
        saveStartNo = imgNo.DEF_START_IMG_NO
        if data.get('saveStartNo'):
            if imgNo.RE_OBJ_IMG_NO.match(data.get('saveStartNo')):
                saveStartNo = data['saveStartNo']
            else:
                return cls.jsonResponse(request, {'msg': 'Invalid StartNo: %s' % data['saveStartNo'], 'status': 1})

        if not os.path.exists(addr):
            return cls.jsonResponse(request, {'msg': 'not a valid image file or folder', 'status': 1})
        if not os.path.isdir(toAddr):
            return cls.jsonResponse(request, {'msg': 'targetAddr must be folder', 'status': 1})

        imgUrls = []
        svImgExt = None
        if os.path.isfile(addr):
            imgExt = imghdr.what(addr)
            if imgExt not in IMG_SUPPORTS:
                return cls.jsonResponse(request, {'msg': 'only support image formats: %s' % IMG_SUPPORTS, 'status': 1})
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
            return cls.jsonResponse(request, {'msg': 'not find images with the path', 'status': 1})
        if not svImgExt:
            svImgExt = DEFAULT_IMG_EXT

        # generae save names of image
        saveNos = imgNo.geneImgNos(saveStartNo, num=len(imgUrls))
        # process the images
        for img, snm in zip(imgUrls, saveNos):
            # beauty
            imgData = Image.open(img)
            if vBrght is not None:
                imgData = imgBeauty.brightnessImage(imgData, vBrght)
            if vCntrst is not None:
                imgData = imgBeauty.contrastImage(imgData, vCntrst)
            # save
            svImgPath = os.path.join(toAddr, "%s.%s" % (snm, svImgExt))
            imgData.save(svImgPath)
            # move to backbend folder
            shutil.move(img, moveAddr)
        return cls.jsonResponse(request, {'status': 0, 'imgNo': saveNos})
