FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app/ /code/app/
COPY ./run.py /code/run.py

EXPOSE 80

CMD [ "python", "run.py" ]