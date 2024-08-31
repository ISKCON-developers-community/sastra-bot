FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
VOLUME [ "/usr/src/app/files" ]
CMD ["python3", "sastrabot.py"]
