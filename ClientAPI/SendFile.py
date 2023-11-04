import os

def handle_fetch_request(clientSocket, repoPath):
    fname = clientSocket.recv(1024).decode('utf-8')

    with open(os.path.join(repoPath, fname), 'r', encoding='utf-8') as file:
        for line in file:
            clientSocket.sendall(line.encode('utf-8'))

    clientSocket.close()