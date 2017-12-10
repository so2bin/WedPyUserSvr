import win32print
import win32ui
from PIL import Image
from PIL import Image, ImageWin

def printImg(imgUrl):
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
    bmp = Image.open (file_name)
    if bmp.size[0] > bmp.size[1]:
        bmp = bmp.rotate (90)

    ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
    scale = min (ratios)
    hDC.StartDoc (file_name)
    hDC.StartPage ()
    dib = ImageWin.Dib (bmp)
    scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
    x1 = int ((printer_size[0] - scaled_width) / 2)
    y1 = int ((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))
    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()


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
    def print(cls, imgUrl):
        return printImg(imgUrl)
