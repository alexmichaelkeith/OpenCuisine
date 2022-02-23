FROM mysql/mysql-server:latest
WORKDIR /db

RUN go get -d -v golang.org/x/net/html  
COPY init.sql /db/


RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .


FROM python:latest
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY main.py /app
CMD python main.py