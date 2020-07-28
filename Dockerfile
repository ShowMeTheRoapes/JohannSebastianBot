FROM python:3.7
WORKDIR /program
COPY . .
RUN pip install -r requirements.txt
RUN ls ./app

CMD ["python", "-u", "./app/bot.py"]