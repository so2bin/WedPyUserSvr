###########################################
#  base http handler
import json
import exceptions

class BaseHandler(object):
    @classmethod
    def doGet(cls, request):
        raise exceptions.NotImplementationError('doGet method is not impleted')

    @classmethod
    def doPost(cls, request):
        raise exceptions.NotImplementationError('doGet method is not impleted')

    @classmethod
    def jsonResponse(cls, request):
        """
        response json with dict data
        """
        if not request.data:
            return
        if isinstance(request.data, (list, dict)):
            data_str = json.dumps(request.data)
        elif isinstance(request.data, str):
            data_str = request.data
        else:
            assert data_str, \
                "json response data must be dict/str/list type but: %s" % type(request.data)

        # Send response status code
        request.send_response(200)
        # Send headers
        request.send_header('Content-type','application/json')
        request.end_headers()
        # Write content as utf-8 data
        request.wfile.write(bytes(data_str, "utf8"))
        return
