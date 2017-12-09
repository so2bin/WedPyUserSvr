##############################################
# 打印图片
from . import tools

def doGet(self):
    tools.printImg.print(self.queryParams['imgUrl'])
    self.send_response(200)

    # Send headers
    self.send_header('Content-type','text/html')
    self.end_headers()

    # Send message back to client
    message = "success!"
    # Write content as utf-8 data
    self.wfile.write(bytes(message, "utf8"))
    return


def d0Post(self):
    pass
