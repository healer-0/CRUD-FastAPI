# CRUD-FastAPI
A simple FastAPI app with PostgreSQL integration, fully containerized using Docker.

## Features
- FastAPI backend
- PostgreSQL database
- SQLAlchemy ORM
- Docker and Docker Compose setup
- .env-based configuration

## Setup

### For local 
```shell
# Create a virtual enviroment

python3 -m venv env
source env/bin/activate
use sample.env file
     
# Install dependencies

pip install -r requirements.txt
      
# also run pre-commit install when contributing to codebase [optional]
    
pre-commit install
      
# Done
```

### For Docker
```shell
   - Use Docker.env file
   - docker-compose up -d
```
Navigate to http://localhost:8000/docs/
