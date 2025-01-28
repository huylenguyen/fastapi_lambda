FROM public.ecr.aws/lambda/python:3.10

# copy application files
COPY ./app ${LAMBDA_TASK_ROOT}/app

# copy poetry and README
COPY pyproject.toml ./
COPY README.md ./

# install poetry and environment
RUN pip install poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install --no-root

# Create Lambda handler
CMD [ "app.main.handler" ]
