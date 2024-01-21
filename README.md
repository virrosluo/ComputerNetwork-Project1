# ComNet_Project1 API

## Getting Started

Follow these steps to set up and run the ComNet_Project1 API:

### 1. Clone the Repository

```bash
git clone [[repository-url]](https://github.com/virrosluo/ComNet_Project1/tree/webService)https://github.com/virrosluo/ComNet_Project1/tree/webService
cd ComNet_Project1
```

### 2. Install the necessary package
```bash
pip install -r requirements.txt
```

### 3. Run the Server Backend with port 8001
```bash
uvicorn Server_main:app --port 8001
```
On mac
```bash
python3 -m uvicorn Server_main:app --port 8001
```

### 4. Run the Client Backend with port 9000
```bash
uvicorn Client_main:app --port 9001
```

On mac
```bash
python3 -m uvicorn Client_main:app --port 9001
```

### 5. Run the Server and Client Frontend
```bash
cd ClientUI
npm run dev
cd ../
cd ServerUI
npm run dev
cd ../
```

### Some Requirement for the app to run properly
- The Server_main and Client_main must be run before you can start the actuall client and server
- The server must be start before the client
- Remember to change the constant server IP
- The FileDirectory are atcually the full file directory: "C:\Users\levie\Downloads\logo.png"
- The New file name is the new file name you want to save as: NewFetchlogo.png