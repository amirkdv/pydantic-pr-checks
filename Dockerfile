FROM python:3.9-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY sections.py .
COPY action.yml .

CMD ["python3", "/app/sections.py"]
