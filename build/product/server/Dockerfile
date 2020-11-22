FROM python:3.7

COPY ./build/product/server/requirements requirements

RUN pip3 install -r ./requirements && rm requirements

COPY ./source/ app

WORKDIR app

EXPOSE 8000