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
│   ├── config # Defines configuration parameters
│   │   ├── __init__.py
│   │   └── settings.py # base settings
│   ├── crud # Defines CRUD operations
│   │   └── __init__.py
│   ├── database # Defines database models
│   │   └── __init__.py
│   ├── external # Defines functions requiring external services
│   │   └── __init__.py
│   ├── routers # Defines routes and endpoints
│   │   └── __init__.py
│   ├── schemas # Defines Pydantic schemas
│   │   └── __init__.py  
│   └── utils # Utilities
│   │   └── __init__.py
├── tests 
│   │   └── __init__.py
├── Dockerfile # Lambda container template
├── pyproject.toml # application Python dependencies
├── env.template # template for environment variables
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

## AWS Lambda usage

In this section, we will deploy the application as an AWS Lambda function and invoke it via a Lambda Function URL. For some context, you can read [this](https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/) nice blog post.

Set up your AWS credentials with 

```bash
aws configure
```

Make a new [ECR registry] with some `<registry_name>` and make note of the `<repository_URI>`, which should be something like `$AWS_ID.dkr.ecr.eu-west-2.amazonaws.com/<registry_name>`.

Then we want to save a couple of variables for use later:

```bash
AWS_ID=$(aws sts get-caller-identity --query 'Account' --output text)
AWS_REGION=$(aws configure get region)
COMMIT_HASH=$(git rev-parse --short HEAD)
REGISTRY_URI=$AWS_ID.dkr.ecr.$AWS_REGION.amazonaws.com/huy-test
```

Ensure you have Docker Engine or Docker Desktop running. Authenticate Docker with AWS with:

```bash
aws ecr get-login-password | docker login -u AWS --password-stdin "https://$AWS_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
```

We'll build the Lambda and upload it into the ECR:

```bash
docker build -t <image_name>:$COMMIT_HASH
docker tag <image_name>:$COMMIT_HASH $REGISTRY_URI:$COMMIT_HASH
docker push $REGISTRY_URI:$COMMIT_HASH
```

Go to [AWS Lambda](https://aws.amazon.com/lambda/) in the Management Console and choose `Create Function` (top right button) -> Select `Container Image` (selection box) -> Choose a name and the ECR image -> `Create Function`. 

Note that the architecture of the Docker container must match the Lambda architecture during creation. If you are on a MacOS with Apple Silicon, choose `arm64`. If you get this wrong, the Lambda invocation will always return `502 Bad Gateway` errors. 

In the management page of the newly created Lambda, choose the `Configuration` tab -> `Function URL` section -> `Create Function URL`. Choose whatever authentication method suits you. For quick prototyping `NONE` is fine. This will automatically create resource access policies for public access. Near the top of the page there will now be a `Function URL`. 

You can now invoke the lambda directly with 
```bash
curl -X 'GET' \
  '<function_url>' \
  -H 'accept: application/json'
```

An example POST endpoint is available at `/example` which just adds two numbers together. Invoke the FastAPI application on this Lambda with:
```bash
curl -X 'POST' \
  '<function_url>/example' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "a": 0,
  "b": 0
}'
```

It's worth noting that newly created Lambdas have a timeout of 3 seconds. If your application takes longer to run, you can increase this up to 15 minutes. 

## AWS SAM usage
In this section, we will deploy the application as an AWS Lambda function and invoke it via AWS API Gateway. For ease of use, we will perform configuration and deployment through [Serverless Framework](https://www.serverless.com/framework/docs/getting-started)

TODO