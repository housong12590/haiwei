FROM python:3.6-alpine

COPY . /project

WORKDIR /project

RUN cd /project \
    && mkdir -p ~/.pip \
    && echo '[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple' > ~/.pip/pip.conf \
    && python -m venv venv \
    && venv/bin/pip install -r requirements.txt -i https://pypi.doubanio.com/simple\
    && venv/bin/pip install gunicorn \
    && export FLASK_APP=manage.py \
    && chmod +x docker-entrypoint.sh

EXPOSE 5000


ENTRYPOINT ["./docker-entrypoint.sh"]


