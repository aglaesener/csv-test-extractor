FROM python:3-alpine

ADD extractor.py /

RUN pip install flask

CMD [ "python", "./extractor.py" ]