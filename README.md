# fastapi_lambda
Template repository for organising and deploying a fastAPI application on AWS Lambda

## Quickstart
Install [Poetry](https://python-poetry.org/), then install Python virtual environment with 

```bash
poetry install
```

Start the application locally with 

```bash
poetry run uvicorn app.main:app --reload
```

## App Structure

```python
.
├── app  # Contains the main application files.
│   ├── __init__.py
│   ├── main.py # Initializes the FastAPI application.
│   ├── dependencies.py # Defines router dependencies
│   ├── routers # Defines routes and endpoints
│   │   └── __init__.py
│   ├── crud # Defines CRUD operations
│   │   └── __init__.py
│   ├── schemas # Defines Pydantic schemas
│   │   └── __init__.py  
│   ├── database # Defines database models
│   │   └── __init__.py
│   ├── external_services # Defines functions requiring external services
│   │   └── __init__.py
│   ├── config # Defines configuration parameters
│   │   ├── __init__.py
│   │   └── settings.py # base settings
│   └── utils # Utilities
│   │   └── __init__.py
├── tests 
│   │   └── __init__.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Docker Usage

Ensure you have Docker Engine or Docker Desktop running. Build the application into a lambda Docker image with 

```bash
docker build -t <image_name>
```

You can choose an arbitrary `<image_name>`. Run the Docker image locally with

```bash
docker run -p 9000:8080 <image_name>
```

Now you can send a local GET request to the test the endpoint with:

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{
    "resource": "/", 
    "path": "/", 
    "httpMethod": "GET", 
    "requestContext": {}, 
    "multiValueQueryStringParameters": null
}'
```

An example POST endpoint is available at `/example` which just adds two numbers together. Invoke this endpoint with:

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
-H "Content-Type: application/json" \
-d '{ 
    "resource": "/example", 
    "path": "/example",
    "httpMethod": "POST",
    "requestContext": {},
    "multiValueQueryStringParameters": null,
    "body": "{\"a\": \"0.1\", \"b\": \"0.2\"}"
}'
```