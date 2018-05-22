import logging
from NIRS.celery import app



@app.task
def send_email():

