##############################################
# 默认

def doGet(self):
    print(self.path, self.queryString, self.queryParams)
    # Send response status code
    self.send_response(200)

    # Send headers
    self.send_header('Content-type','text/html')
    self.end_headers()

    # Send message back to client
    message = "Hello world!"
    # Write content as utf-8 data
    self.wfile.write(bytes(message, "utf8"))
    return


def d0Post(self):
    pass
