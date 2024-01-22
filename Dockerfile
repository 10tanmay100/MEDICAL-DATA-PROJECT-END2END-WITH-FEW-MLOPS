FROM python:3.8
COPY . /app1
WORKDIR /app1
RUN pip install -r requirements_dev.txt
CMD ["python","app.py"]