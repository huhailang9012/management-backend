FROM python:3.8

MAINTAINER Jerry<huhailang@yahoo.cn>
RUN pip install fastapi uvicorn requests -i https://mirrors.aliyun.com/pypi/simple/
WORKDIR /code
COPY docker/api /code/
RUN cd /code

CMD uvicorn controller:app --reload --port 8000 --host 0.0.0.0