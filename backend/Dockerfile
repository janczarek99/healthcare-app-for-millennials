FROM python:3.9.7-slim-buster

# Wait for it etc.
RUN apt update && \
    apt install -y wait-for-it && \
    apt-get -y autoremove && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

# Python packages
RUN pip install pip==21.2.4
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

WORKDIR /app

# Alembic
# COPY alembic.ini .
# COPY ./alembic ./alembic

# Seeds
# COPY ./seeds ./seeds/

# Application
COPY ./src ./src/
COPY run.py .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
