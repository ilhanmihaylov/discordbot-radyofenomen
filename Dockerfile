FROM python:3.6.9-buster

RUN apt update -y
RUN apt install ffmpeg -y

RUN mkdir /opt/fenomenbot
COPY * /opt/fenomenbot/

RUN pip install -r /opt/fenomenbot/requirements.txt

CMD ["python", "/opt/fenomenbot/main.py"]

