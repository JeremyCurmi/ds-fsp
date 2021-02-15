FROM python:3.7-slim
COPY . /usr/app/
EXPOSE 8000
WORKDIR /usr/app/
RUN pip install -r requirements.txt
CMD python predictor.py