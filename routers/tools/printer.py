import os
import imghdr
import win32print
import win32ui
from PIL import Image
from PIL import Image, ImageWin

from config import IMG_SUPPORTS

# 剪切比例的精度
CUT_PERCISION = 10

def calcCutInfo(orw, orh, cutOpt):
    """
    计算剪切边与边距值
    """
    rw = cutOpt['w']
    rh = cutOpt['h']
    scaledW = (rw*orh)/rh
    if abs(orw - scaledW) < CUT_PERCISION:
        return None, 0, orw, orh
    if orw > scaledW:
        # cut w
        newW = scaledW
        dw = round((orw - newW)/2, 2)
        return 'W', dw, round(newW), orh
    else:
        # cut h
        newH = (rh*orw)/rw
        dh = round((orh - newH)/2, 2)
        return 'H', dh, orw, newH

def cutImg(imgData, _type, dv, newW, newH):
    """
    剪切指定宽度
    @params _type: W, H
    """
    if _type == 'W':
        imgData.crop((dv, 0, newW, newH))
    elif _type == 'H':
        imgData.crop((0, dv, newW, newH))
    return imgData


def zoomImg(imgData, printW, printH):
    """
    等比例绽放
    """
    ratios = [1.0 * printW / imgData.size[0], 1.0 * printH / imgData.size[1]]
    scale = min (ratios)
    return round(imgData.size[0]*scale), round(imgData.size[1]*scale)


def conbineImgs(upImgData, lowImgData, opt):
    """
    合成图片，将upimg黏贴到lowimg上，位置与尺寸参数在opt
    @params upImgData: 上层图片
    @params lowImgData: 背景图片
    @params opt: {box: (x, y, w, h), imgArea: (w, h)}
                 imgArea为上层图片黏贴范围 box为背景目标可黏贴范围
    """
    x = opt['box'][0]
    y = opt['box'][1]
    w = opt['box'][2]
    h = opt['box'][3]
    if opt.get('imgArea'):
        upImgData = upImgData.crop((0,0,opt['imgArea']['w'],opt['imgArea']['h']))
    region = upImgData
    region = region.resize((w, h))
    lowImgData.paste(region, (x, y, w+x, y+h))
    return lowImgData


def preProcessImg(imgUrl, templateUrl, cutOpt, composeOpt):
    """
    预处理照片
    @params imgUrl: 处理照片
    @params templateUrl: 模板照片
    @params cutOpt: 剪切比例 {w: 3, h: 2}
    @params composeOpt: 合成参数 (x,y,w,h)  距左上角距离(x,y)与像素宽高(w,h)
    """
    img = Image.open(imgUrl)
    orw = img.size[0]
    orh = img.size[1]
    if orw > orh:
        img = img.rotate(90, expand=True)
        orw, orh = orh, orw

    # 按比例剪切
    cedge, dv, newW, newH = calcCutInfo(orw, orh, cutOpt)
    if cedge:
        img = cutImg(img, cedge, dv, newW, newH)
    return img


def printImg(imgUrl, templateUrl, cutOpt, composeOpt):
    """
    预处理照片
    @params imgUrl: 处理照片
    @params templateUrl: 模板照片
    @params cutOpt: 剪切比例 {w: 3, h: 2}
    @params composeOpt: 合成参数 (x,y,w,h)  距左上角距离(x,y)与像素宽高(w,h)
    """
    if not imgUrl or not templateUrl:
        return None
    if not os.path.isfile(imgUrl) or imghdr.what(imgUrl) not in IMG_SUPPORTS \
        or not os.path.isfile(templateUrl) or imghdr.what(templateUrl) not in IMG_SUPPORTS:
        return None
    imgDir, imgName = os.path.split(imgUrl)
    HORZRES = 8
    VERTRES = 10
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    PHYSICALOFFSETX = 112
    PHYSICALOFFSETY = 113
    printer_name = win32print.GetDefaultPrinter ()
    file_name = imgUrl
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC(printer_name)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)
    # 预处理
    imgData = preProcessImg(imgUrl, templateUrl, cutOpt, composeOpt)
    #合成图片
    lowImgData = Image.open(templateUrl)
    (x, y, w, h) = composeOpt

    if lowImgData.size[0] > lowImgData.size[1]:
        lowImgData = lowImgData.rotate(90, expand=True)
        x, y = y, x
        w, h = h, w

    cnbImg = conbineImgs(imgData, lowImgData, {
        'box': (x, y , w, h)
    })
    # cnbImg.show()
    # zoom
    scaled_width, scaled_height = zoomImg(cnbImg, printer_size[0], printer_size[1])

    hDC.StartDoc (file_name)
    hDC.StartPage ()
    dib = ImageWin.Dib (imgData)
    x1 = int ((printer_size[0] - scaled_width) / 2)
    y1 = int ((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))
    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()
    return imgName


#########################################
# https://msdn.microsoft.com/en-us/library/cc244669.aspx

# 枚举本地打印机
PRINTER_ENUM_LOCAL = 0x00000002
# 枚举由name参数指定的打印机。其中的名字可以是一个供应商、域或服务器。如name为NULL，则枚举出可用的打印机
PRINTER_ENUM_NAME = 0x00000008
# 枚举共享打印机
PRINTER_ENUM_SHARED =  0x00000020


class Printer(object):
    @classmethod
    def GetDefaultPrinter(cls):
        return win32print.GetDefaultPrinter()



class ImgPrinter(object):
    @classmethod
    def enumPrinters(cls, flag=PRINTER_ENUM_LOCAL, name=None, lvl=1):
        """
        @return: (flags, description, name, comment)
        """
        # printer enum flag:
        return win32print.EnumPrinters(flag, name, lvl)

    @classmethod
    def print(cls, imgUrl, templateUrl, cutOpt, composeOpt):
        return printImg(imgUrl, templateUrl, cutOpt, composeOpt)
