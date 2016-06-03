import zmq

class RemoteStarCraftGame(object):

    def __init__(self):
        context = zmq.Context()
        #  Socket to talk to server
        print("Connecting to hello world server...")
        self.socket = context.socket(zmq.REQ)

        windows_server_2012_url = "tcp://0.tcp.ngrok.io:12449"
        self.socket.connect(windows_server_2012_url)


    def make_action(self, action_payload):
        """Makes an action from a payload and returns a dump of the screen"""
        print("Sending request %s ..." % action_payload)
        self.socket.send_json(action_payload)

        #  Get the reply.
        message = self.socket.recv()
        print("Received reply [ %s ]" % (message))
        return message
        pass
