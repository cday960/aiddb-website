---
layout: page
title: "Getting Started"
nav_order: 2
---

# Getting Started
### 1. `.env` file
Ask me to send you the `.env` file, this is necessary for encryption and app secret keys. Place env file in project directory, same folder as `run.py`.

### 2. Virtual Environment
In project directory, create virtual environment
```
python -m venv .venv
```
This creates your virtual environment in the folder `.venv`

### 3. Activate environment

#### Linux-
```
source .venv/bin/activate
```

Windows-
```
.\.venv\Scripts\activate.bat
```
### 4. Install MS C++ Build Tools

https://visualstudio.microsoft.com/visual-cpp-build-tools/

Make sure to install "Desktop development with C++" and "Node.js build tools".

### 5. Install Python packages
```
pip install -r requirements.txt
```

### 6. Run the server
```
python run.py
```
You can now connect to the dev site at http://127.0.0.1:5000

---


## Commands

### Run server
`python app.py`

### Start Redis server
```
sudo systemctl enable --now redis-server
```

```
redis-cli ping
```
should give a response `PONG`


### Normal Test
To run the test suite, in `/website` run
```
pytest
```

### Coverage Test
```
pytest --cov=app --cov=util
```
