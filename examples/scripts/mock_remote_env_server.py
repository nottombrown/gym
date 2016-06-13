import json
import zmq
from gym.envs.starcraft.tests.helper import TestData
import logging
logger = logging.getLogger(__name__)


def _bind_zmq_socket():
    context = zmq.Context()
    logger.info("Starting StarCraftLearningEnv API Server...")
    zmq_socket = context.socket(zmq.REP)
    zmq_socket.bind("tcp://*:3000")
    return zmq_socket


def _listen(socket):
    (endpoint, headers_json, body_json) = socket.recv_multipart()
    logger.info("Received request: \n    {}\n    {}\n    {}".
                format(endpoint, headers_json, body_json))

    (status, headers, body) = TestData.step_env_response()
    headers_json = json.dumps(headers)
    body_json = json.dumps(body)

    logger.info("Sending response: \n    {}\n    {}\n    {}\n\n".
                format(status, headers_json, body_json[:300]))

    response = (status, headers_json, body_json)
    socket.send_multipart(response)

if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    socket = _bind_zmq_socket()
    while True:
        _listen(socket)
