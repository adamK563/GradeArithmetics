FROM python:3.10.8

COPY . /RapidoAPI
WORKDIR /RapidoAPI

RUN pip install -r requirments.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#docker build -t rapido_api .
#docker run -p 8000:8000 rapido_api