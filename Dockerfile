FROM rushidhar/pro:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD python3 /app/update.py && gunicorn -b 0.0.0.0:8003 api.app:app

# CMD python3 /app/update.py && gunicorn -b 0.0.0.0:8003 --timeout 0 -k gevent api.app:app

CMD ["bash", "start.sh"]
