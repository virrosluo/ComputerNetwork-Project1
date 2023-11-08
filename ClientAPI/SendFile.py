import os

def handle_fetch_request(clientSocket, repoPath):
    fname = clientSocket.recv(1024).decode('utf-8')
    
    with open(os.path.join(os.getcwd(), repoPath, fname), 'rb') as file:
        for line in file:
            clientSocket.sendall(line)

    clientSocket.close()