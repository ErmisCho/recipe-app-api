#alpine is a lightweight version of Linux, so it's ideal to run Linux containers
FROM python:3.9-alpine3.13
LABEL maintainer="ermis"

#Do not buffer the output
ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# we could add multiple RUN commands but then we would have multiple image layers

# create a virtual Python environment for our project for any conflicting dependencies of our project
# and other project dependencies in the docker image 

# if this Dockerfile runs through the docker-compose.yml, then the ARG from there is going to prevail
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    #it will install inside the venv because we are specifying the full path for pip inside our venv
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

#switch from root to django-user, so the application runs from the user 'django-user'
USER django-user