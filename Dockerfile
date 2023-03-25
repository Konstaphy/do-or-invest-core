FROM python:3.10
WORKDIR /usr/app
COPY . .
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/app/"

CMD [ "python3", "src/main.py" ]