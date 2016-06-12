import zmq
import json

class RemoteEnvAPIRequestor(object):
    """
    We emulate HTTP over zmq - Messages are sent as tuples of three strings.
    The body is always gzipped.

    Request Format:
        A tuple of the following three strings:

        - request - A string emulating an HTTP request
        - headers - a JSON-encoded object
        - body - a JSON-encoded object

    Example Request:
        ("POST /v1/endpoint", "{header_name: value}", "body")

    Response Format:
        A tuple of the following three strings:

        - status - A string emulating HTTP status
        - headers - a JSON-encoded object
        - body - a JSON-encoded object


    Example Response (success):
        ("200", "{header_name: value}", "body")


    Example Response (error):
        ("500", "{header_name: value}", '{
            "error": "NoAvailableWorkersException",
            "error_message": "15/15 starcraft_env_workers are currently running episodes."
        }')
    """
    @classmethod
    def _open_zmq_socket(cls):
        context = zmq.Context()
        print("Connecting to StarCraftServer...")
        socket = context.socket(zmq.REQ)

        windows_server_2012_url = "tcp://0.tcp.ngrok.io:19085"
        socket.connect(windows_server_2012_url)
        return socket

    @classmethod
    def request(cls, endpoint, headers, body):
        """
        Args:
            (endpoint, headers, body)

        Returns:
            (status, headers, body)
        """
        # TODO: Find a place to handle errors
        # TODO: Find a place to set headers
        # TODO: How should we address security - certs etc.

        request = (
            endpoint,
            json.dumps(headers),
            json.dumps(body),
        )

        socket = cls._open_zmq_socket()
        socket.send_multipart(request)
        status, response_headers, response_body = socket.recv_multipart(request)

        # Socket is closed automatically during GC, but we do it anyway to be safe
        socket.close()

        print("Response %s" % status)

        return (
            status,
            json.loads(response_headers),
            json.loads(body)
        )