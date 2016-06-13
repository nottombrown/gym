import json
import zmq
from gym.envs.starcraft.tests.helper import TestData

def _bind_zmq_socket():
    context = zmq.Context()
    print("Starting StarCraftLearningEnv API Server...")
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:3000")
    return socket


def _listen(socket):
    (endpoint, headers_json, body_json) = socket.recv_multipart()
    print("Received request: \n")
    print(endpoint)
    print(headers_json)
    print(body_json)

    (status, headers, body) = TestData.step_env_response()
    headers_json = json.dumps(headers)
    body_json = json.dumps(body)

    print("\n Sending response: ")
    print(status)
    print(headers_json)
    print(body_json[:200])
    print("\n\n")

    response = (status, headers_json, body_json)
    socket.send_multipart(response)

if __name__ == '__main__':
    socket = _bind_zmq_socket()
    for i in range(10):
        _listen(socket)
