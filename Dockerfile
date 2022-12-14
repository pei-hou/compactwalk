FROM python:3.8.3

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app

CMD [ "python", "exp_all.py" ]