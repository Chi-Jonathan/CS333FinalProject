FROM python:3.10

COPY . .

CMD ["python3", "./main.py"]