FROM python:3.12-slim

WORKDIR /job

COPY job.py .

RUN pip install pandas matplotlib

CMD ["python", "job.py"]