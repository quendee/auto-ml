FROM python:3.7.9
RUN apt-get update && apt-get install -y python3-dev build-essential

COPY . / mlapp/
RUN make /mlapp
WORKDIR "/mlapp"

RUN pip install -r requirements.txt

# docker build --rm -t "mlpipe:latest" .
# docker-compose rm -fs
# docker-compose up --build -d