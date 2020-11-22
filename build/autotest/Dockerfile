FROM python:3.7

COPY ./build/autotest/requirements requirements

RUN pip3 install -r ./requirements && rm requirements

COPY ./tests/ tests

WORKDIR tests

EXPOSE 8000