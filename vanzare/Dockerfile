FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
ADD requirements.txt /code/
ADD requirements /code/requirements
WORKDIR /code
RUN pip install -r requirements.txt
