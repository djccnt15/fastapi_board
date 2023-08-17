FROM python:3.10

EXPOSE 8000

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN echo Asia/Seoul > /etc/timezone

RUN apt-get update
RUN apt-get install -y vim

RUN mkdir fastboard
WORKDIR fastboard/

COPY ./ ./

RUN pip install --no-cache-dir -r ./requirements/test.txt

# ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "main:app", "--reload" ]
ENTRYPOINT [ \
    "gunicorn", "main:app", \
    "--workers", "2", \
    "--worker-class", "uvicorn.workers.UvicornWorker", \
    "--bind", "0.0.0.0", \
    "--log-config", "/fastboard/logs/uvicorn_log.ini" \
 ]