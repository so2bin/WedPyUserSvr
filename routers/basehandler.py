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
    def jsonResponse(cls, request, response=None, status=200):
        """
        response json with dict data:
            response or request.response
        """
        data = response or request.response
        if not data:
            data = ""

        if isinstance(data, (list, dict)):
            data_str = json.dumps(data)
        elif isinstance(data, str):
            data_str = data
        else:
            assert data_str, \
                "json response data must be dict/str/list type but: %s" % type(data)

        # Send response status code
        request.send_response(status)
        # Send headers
        request.send_header('Content-type','application/json')
        request.end_headers()
        # Write content as utf-8 data
        request.wfile.write(bytes(data_str, "utf8"))
        return
