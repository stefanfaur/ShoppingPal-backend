FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./test_api.sh /code/test_api.sh

COPY ./app /code/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","80"]

