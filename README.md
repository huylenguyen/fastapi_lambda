# fastapi_lambda
Template repository for organising and deploying a fastAPI application on AWS Lambda with local Docker testing.

## Quickstart
Install [Poetry](https://python-poetry.org/), then install Python virtual environment with 

```bash
poetry install
```

Start the application locally with 

```bash
poetry run uvicorn app.main:app --reload
```

Now you can send a local GET request to the test the main endpoint with:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json'
```

An example POST endpoint is available at `/example` which just adds two numbers together. Invoke this endpoint with:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/example' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "a": 0,
  "b": 0
}'
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

Since the FastAPI application is now wrapped by the Lambda handler in the Docker image, you need to amend the request format a bit compared to the previous section. To test the GET endpoint:
```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{
    "resource": "/", 
    "path": "/", 
    "httpMethod": "GET", 
    "requestContext": {}, 
    "multiValueQueryStringParameters": null
}'
```

To test the POST endpoint:
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

## AWS Lambda usage

For some context, you can read [this](https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/) nice blog post.

Set up your AWS credentials with 

```bash
aws configure
```

Then we want to save a couple of variables for use later:

```bash
AWS_ID=$(aws sts get-caller-identity --query 'Account' --output text)
AWS_REGION=$(aws configure get region)
COMMITHASH=$(git rev-parse --short HEAD)
```

Make a new [ECR registry] with some `<registry_name>` and make note of the `<repository_URI>`, which should be something like `$AWS_ID.dkr.ecr.eu-west-2.amazonaws.com/<registry_name>`.

Ensure you have Docker Engine or Docker Desktop running. Authenticate Docker with AWS with:

```bash
aws ecr get-login-password | docker login -u AWS --password-stdin "https://$AWS_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
```

We'll build the Lambda and upload it into the ECR:

```bash
docker build -t <image_name>::$COMMITHASH
docker tag <image_name>:$COMMITHASH <ecr_uri>/<image_name>:$COMMITHASH
docker push <ecr_uri>/<image_name>:$COMMITHASH
```