# MedicalReceptionAgent with langchain

Project description goes here.

## Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- [Redis](https://redis.io/download)
- [RabbitMQ](https://www.rabbitmq.com/download.html) (for Celery task queue)
- Git (optional, but recommended)

## Setup

### 1. Clone the Repository

```bash
git clone git@github.com:RtjShreyD/excelus_agents.git
cd excelus_agents/medical_reception
```

### 2. Create a Virtual Environment

#### On Windows

```bash
virtualenv venv
venv\Scripts\activate
```

#### On Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

#### On Windows

```bash
set OPENAI_API_KEY=openai-api-key
set CELERY_BROKER_URL=pyamqp://<username>:<password>@<rabbitm-mq-host>:<rabbit-mq-port>/<vhostname>
set CELERY_RESULT_BACKEND=redis://localhost:6379/0
set REDIS_MEMORY_SERVER_URL=redis://localhost:6379/1
set REDIS_DATA_SERVER_IP=localhost
set REDIS_DATA_SERVER_PORT=6379
set REDIS_DATA_SERVER_DB=2
```

#### On Linux/macOS

```bash
export OPENAI_API_KEY=openai-api-key
export CELERY_BROKER_URL=pyamqp://<username>:<password>@<rabbitm-mq-host>:<rabbit-mq-port>/<vhostname>
export CELERY_RESULT_BACKEND=redis://localhost:6379/0
export REDIS_MEMORY_SERVER_URL=redis://localhost:6379/1
export REDIS_DATA_SERVER_IP=localhost
export REDIS_DATA_SERVER_PORT=6379
export REDIS_DATA_SERVER_DB=2
```

### 5. Run the Server

```bash
uvicorn main:app --reload --port 8001
```

## Routes

### 1. **Initialization Endpoint**

- **Endpoint:** `/initialise`
- **Method:** POST
- **Description:** Initializes resources and returns a session ID and agent response.
- **Request Body:**
  ```json
  {
    "session_id": "optional-session-id"
  }
  ```
- **Response:**
  ```json
  {
    "status": 201,
    "msg": "Initialized",
    "details": {
      "session_id": "generated-or-input-session-id",
      "agent_response": "initialization-response"
    }
  }
  ```

### 2. **Chat Functionality Endpoint**

- **Endpoint:** `/chat`
- **Method:** POST
- **Description:** Implements chat functionality and returns agent response.
- **Request Body:**
  ```json
  {
    "session_id": "session-id",
    "human_message": "user-input-message"
  }
  ```
- **Response:**
  ```json
  {
    "status": 200,
    "msg": "Success",
    "details": {
      "session_id": "session-id",
      "agent_response": "agent-response-message"
    }
  }
  ```

## API Documentation

API documentation is available using Swagger UI at `http://localhost:8001/docs`. You can interact with the API endpoints, view request/response examples, and explore the available routes using this documentation interface.

---

Feel free to customize the README according to your specific project details and requirements. This template provides a basic structure to get you started.