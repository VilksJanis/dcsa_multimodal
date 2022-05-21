FROM python:3.10

COPY requirements.txt ./
RUN pip install gunicorn==20.0.4
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /src
WORKDIR /src/

EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-t", "120", "-b", "0.0.0.0:8080", "unicorn:app"]