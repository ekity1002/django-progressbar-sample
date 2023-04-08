# # our base image
FROM python:3.9.16-buster

# install Python modules needed by the Python app
COPY ./requirements.txt /app/
RUN pip install -U pip && \
    pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
