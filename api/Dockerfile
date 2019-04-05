FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod +x /code/docker-entrypoint.sh
RUN sed -i -e 's/\r$//' docker-entrypoint.sh