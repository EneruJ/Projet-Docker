FROM python:latest

RUN pip install fastapi uvicorn pytest requests pymysql mysql-connector-python httpx
RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
RUN ["pytest", "/app"]
