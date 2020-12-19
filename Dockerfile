FROM python:3.8

MAINTAINER Jerry<huhailang@yahoo.cn>
RUN pip install fastapi uvicorn requests -i https://mirrors.aliyun.com/pypi/simple/
WORKDIR /code
RUN cd /code

CMD uvicorn app:app --reload --port 8000 --host 0.0.0.0