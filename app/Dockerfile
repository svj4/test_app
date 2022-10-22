FROM python:alpine

WORKDIR /app

RUN pip install flask
RUN pip install requests
RUN pip install flask_sqlalchemy 

COPY . .

CMD ["python", "app.py"]