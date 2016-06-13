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

        url = "tcp://localhost:3000"
        socket.connect(url)
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
        print("Sending request: ", request)

        socket = cls._open_zmq_socket()
        socket.send_multipart(request)
        status, response_headers_json, response_body_json = socket.recv_multipart()

        # Socket is closed automatically during GC, but we do it anyway to be safe
        socket.close()

        response_headers = json.loads(response_headers_json)
        response_body = json.loads(response_body_json)

        print("Received response", status, response_headers, response_body_json[:200])

        return (
            status,
            response_headers,
            response_body
        )
