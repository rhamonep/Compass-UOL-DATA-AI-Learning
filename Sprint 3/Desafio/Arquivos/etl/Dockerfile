FROM python:3.12-slim

WORKDIR /etl

COPY etl.py .

RUN pip install pandas

CMD ["python", "etl.py"]
