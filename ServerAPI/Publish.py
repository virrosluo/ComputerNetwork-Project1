import json

def handle_publish(clientAddress, message):
    data = json.loads(message)
    return data['fileName'], (clientAddress[0], data['serverHandlerPort'])