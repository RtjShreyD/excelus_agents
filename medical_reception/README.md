# MedicalReceptionAgent with langchain

Project description goes here.

## Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- [Redis](https://redis.io/download)
- [Another Redis Desktop Manager] 
<!-- - [RabbitMQ](https://www.rabbitmq.com/download.html) (for Celery task queue)
- Git (optional, but recommended) -->

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
Create a new file named .env  and copy contents from .env.example to it (Make sure you are inside the particular agents directory 'medical_reception' in this case)

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