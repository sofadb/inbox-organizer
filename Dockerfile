FROM python:3.11-slim

WORKDIR /app

COPY organize_files.py .

RUN mkdir -p /data/inbox /data/journal

CMD ["python", "organize_files.py"]