class ServerUI:
    def __init__(self):
        pass
  
    def display_publish_file(self, fileList:dict, clientDict:dict):
        for fname, clientList in fileList.items():
            print(f"- {fname}:")
            print('\t'.join([clientDict[clientKey][0] for clientKey in clientList ]))
            print("------------------------------------------------------------------")
  
    def display_available_client(self, clientDict: dict):
        for idx, record in enumerate(clientDict):
            print(f"{idx}: Address: {record['address']} -- Name: {record['name']} -- Server handler Port: {record['serverHandlerPort']} -- Client handler Port: {record['clientHandlerPort']}")

    def display_ping_info(self, result:bool):
        print("Client is alive") if result == True else print("Client is not alive")