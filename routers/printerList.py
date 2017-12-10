##############################################
# 打印机列表输的
import json
from .tools.printer import ImgPrinter
from .tools.printerEnums import PrinterStatus
from routers.basehandler import BaseHandler


class HTTPHandler(BaseHandler):
    @classmethod
    def doGet(cls, request):
        prntrs = ImgPrinter.enumPrinters(lvl=2)
        res = []
        for ptr_obj in prntrs:
            res.append({
                'printerName': ptr_obj['pPrinterName'],
                'portName': ptr_obj['pPortName'],
                'driverName': ptr_obj['pDriverName'],
                'datatype': ptr_obj['pDatatype'],
                'printProcessor': ptr_obj['pPrintProcessor'],
                'status': [ptr_obj['Status'], PrinterStatus.type_to_text(ptr_obj['Status'])]
            })
        request.data = res
        return cls.jsonResponse(request)

    @classmethod
    def d0Post(self, request):
        pass
