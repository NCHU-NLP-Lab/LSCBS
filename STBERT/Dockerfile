FROM python:3.8

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 1025

CMD ["python", "./STBERT_Srv.py"]