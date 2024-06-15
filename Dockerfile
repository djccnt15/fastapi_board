FROM python:3.11

EXPOSE 8000

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN echo Asia/Seoul > /etc/timezone

RUN apt-get update
RUN apt-get install -y vim

RUN mkdir app
WORKDIR /app/
RUN mkdir log

COPY ./ ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements/ops.txt

# ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "main:app" ]
ENTRYPOINT [ \
    "gunicorn", "main:app", \
    "--workers", "1", \
    "--worker-class", "uvicorn.workers.UvicornWorker", \
    "--bind", "0.0.0.0", \
    "--log-config", "/app/resources/log_container.ini" \
 ]