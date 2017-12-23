import os
import imghdr
import win32print
import win32ui
import requests
from io import BytesIO
from PIL import Image, ImageWin

from config import IMG_SUPPORTS

# 剪切比例的精度
CUT_PERCISION = 5

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
        imgData = imgData.crop((dv, 0, newW, newH))
    elif _type == 'H':
        imgData = imgData.crop((0, dv, newW, newH))
    return imgData


def zoomImg(imgData, printW, printH):
    """
    等比例缩放
    """
    ratios = [1.0 * printW / imgData.size[0], 1.0 * printH / imgData.size[1]]
    scale = min (ratios)
    return round(imgData.size[0]*scale), round(imgData.size[1]*scale)


def conbineImgs(upImgData, lowImgData, opt, mask=None):
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
    if mask:
        lowImgData.paste(region, (x, y, w+x, y+h), mask)
    else:
        lowImgData.paste(region, (x, y, w+x, y+h))
    return lowImgData


def preProcessImg(img, tmp):
    """
    预处理照片：
      1. 根据比例剪切成用户选择的照片区域的比例
      2. 缩放照片到用户选择区域映射的尺寸
    @params img: 待处理照片数据
    @params tmp: 模板参数
    """
    orw = img.size[0]
    orh = img.size[1]
    # 按比例剪切
    cutOpt = {'w': tmp['selW'], 'h': tmp['selH']}
    cedge, dv, newW, newH = calcCutInfo(orw, orh, cutOpt)
    if cedge:
        img = cutImg(img, cedge, dv, newW, newH)
    # 缩放到对应的选择区域内
    return img.resize((tmp['selW'], tmp['selH']))


def getConbinedImg(oriImgData, tmpImgData, tmp, bReverse):
    """
    获取合成图片
    @params bReverse: True: 模板在上, False: 模板在下
    """
    # 预处理
    oriImgData = preProcessImg(oriImgData, tmp)
    # 模板所有照片的尺寸需要resize到规定的模板尺寸
    tmpImgData = tmpImgData.resize((tmp['realW'], tmp['realH']))
    (x, y, w, h) = (tmp['sx'], tmp['sy'], tmp['selW'], tmp['selH'])
    # 图片在上
    if not bReverse:
        #合成图片
        cnbImg = conbineImgs(imgData, tmpImgData, {
            'box': (x, y , w, h)
        })
    # 模板在上
    else:
        # 创建一张空白图片先合成原始图片
        nullImg = Image.new('RGBA', (tmp['realW'], tmp['realH']))
        bkImg = conbineImgs(imgData, nullImg, {
            'box': (x, y , w, h)
        })
        # 再与模板进行合成，模板在上，图片在下
        cnbImg = conbineImgs(tmpImgData, bkImg, {
            'box': (0, 0, tmp['realW'], tmp['realH'])
        }, tmpImgData)
    return cnbImg


def printImg(imgUrl, lngTmp, hrTmp, bReverse):
    """
    打印照片，模板在下，照片在上
    @params imgUrl: 处理照片
    @params cutOpt: 剪切比例 {w: 3, h: 2}
    @params composeOpt: 合成参数 (x,y,w,h)  距左上角距离(x,y)与像素宽高(w,h)
    @params bReverse: True: 模板在上, False: 模板在下
    """
    if not imgUrl or not lngTmp or not hrTmp:
        return None
    if not os.path.isfile(imgUrl) or imghdr.what(imgUrl) not in IMG_SUPPORTS:
        return None
    imgData = Image.open(imgUrl)
    if not imgData:
        return None
    imgData = imgData.convert('RGBA')
    # w > h 用横向模板 否则 竖向模板
    if imgData.size[0] > imgData.size[1]:
        tmp = hrTmp
    else:
        tmp = lngTmp

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
    imgData = preProcessImg(imgData, tmp)
    # 模板图片
    tmpUrl = tmp['tmpUrl']
    if tmpUrl.startswith('http'):
        tmpRes = requests.get(tmpUrl)
        tmpUrl = BytesIO(tmpRes.content)
    tmpImgData = Image.open(tmpUrl)
    if not tmpImgData:
        return None
    tmpImgData = tmpImgData.convert('RGBA')
    # 合成
    cnbImg = getConbinedImg(imgData, tmpImgData, tmp, bReverse)
    # cnbImg.save('D:\\Node\\Imgs\\comp\\%s.png' % imgName)
    # return imgName
    # cnbImg.show()
    scaled_width, scaled_height = zoomImg(cnbImg, printer_size[0], printer_size[1])

    hDC.StartDoc (file_name)
    hDC.StartPage ()
    dib = ImageWin.Dib (cnbImg)
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
    def print(cls, imgUrl, lngTmp, hrTmp, bReverse):
        return printImg(imgUrl, lngTmp, hrTmp, bReverse)
