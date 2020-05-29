FROM ubuntu:bionic
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y net-tools iputils-ping nano curl trafficserver
RUN mkdir /var/run/trafficserver
RUN chown -R trafficserver:trafficserver /var/run/trafficserver
EXPOSE 8080