import socket
import sys
import logging
from botan import Core

log = logging.getLogger(__name__)

class ChatScript:
    def __init__(self, host, port, botname):
        config = Core.config.chatscript()
        self.host = config.host
        self.port = config.port
        self.botname = botname
        log.debug('Created: host={}, port={}, botname={}'.format(self.host, self.port, self.botname))

    def say(self, message, username='developer'):
        log.debug('u:{} -> b:{} : "{}"'.format(username, self.botname, message))
        to_say = "{username}\u0000{botname}\u0000{message}\u0000".format(username=username, botname='botan', message=message)

        connection = socket.create_connection((self.host, self.port))
        
        msg_encoded = to_say.encode()
        log.debug('Sending bytes: {}'.format(msg_encoded))
        connection.send(msg_encoded)
        response =  ""
        while True:
            chunk = connection.recv(1024)
            if chunk:
                response += chunk.decode('utf-8', "backslashreplace")
            else:
                break
        log.debug('b:{} -> u:{} : "{}"'.format(self.botname, username, response))
        return response