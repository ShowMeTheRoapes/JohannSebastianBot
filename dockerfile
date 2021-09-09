FROM python:3.7
WORKDIR /program
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-u", "./bot.py"]