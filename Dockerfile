FROM python:3.8-slim
FROM openjdk:11-jdk-slim

RUN apt-get update && apt-get install -y openjdk-11-jdk

RUN set -xe && apt-get -yqq update && apt-get -yqq install python3-pip && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

EXPOSE 80

ENV NAME World


ENTRYPOINT ["java", "-jar", "/app/skyviewmod.jar"]
CMD ['python', 'sky_xml.py']
