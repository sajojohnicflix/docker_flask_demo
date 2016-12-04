FROM ubuntu:latest
MAINTAINER Sajo John "sajo.john@icflix.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential ffmpeg
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask-demo.py"]
