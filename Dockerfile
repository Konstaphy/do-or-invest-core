FROM python:3.10
WORKDIR /usr/app
COPY . .
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/app/"

EXPOSE 8080
CMD [ "python3", "src/main.py" ]