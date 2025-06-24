FROM python:3.11

#working directory di container
WORKDIR /app

#file requirements dan install dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#semua file dari direktori lokal ke dalam container
COPY ./app ./app

#env var buat Flask
ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0

#run server Flask
CMD ["flask", "run"]
