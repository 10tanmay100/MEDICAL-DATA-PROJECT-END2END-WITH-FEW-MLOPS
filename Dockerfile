FROM python:3.11
COPY . /app1
WORKDIR /app1
RUN pip install -r requirements.txt
CMD ["python","app.py"]