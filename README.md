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

### 4. Run the Client Backend with port 9000
```bash
uvicorn Server_main:app --port 9000
```
