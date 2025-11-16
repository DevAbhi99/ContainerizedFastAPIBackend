FROM python:3.12-slim

WORKDIR /app

COPY /Backend/Main.py /app/

COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 4500

CMD ["uvicorn", "Main:api", "--host", "0.0.0.0", "--port", "4500"]