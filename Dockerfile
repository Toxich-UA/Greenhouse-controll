FROM python:3.6

ENV TZ=Europe/Kiev
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install -r requirements.txt

CMD ["python", "controllers/main.py"]
