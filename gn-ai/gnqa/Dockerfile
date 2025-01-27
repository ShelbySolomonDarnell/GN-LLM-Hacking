FROM python:3.10.7
RUN apt update && apt upgrade -y
COPY requirements.txt /opt/app/requirements.txt
RUN pip install --no-cache-dir -r /opt/app/requirements.txt
#RUN pip install --no-cache-dir ragas==0.1.9 r2r==0.3.4 langchain-together==0.2.0 together==1.3.1 pandas==2.1.0

RUN mkdir /code

RUN apt update && apt -y upgrade
RUN apt install -y vim

CMD ["/bin/sh", "-c", "bash"]

