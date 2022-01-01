FROM python:3.9-alpine

RUN mkdir /app
WORKDIR /app
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pr_checks/ pr_checks/
COPY main.py .
COPY action.yml .

CMD ["python3", "/app/main.py", "--output=comment"]
