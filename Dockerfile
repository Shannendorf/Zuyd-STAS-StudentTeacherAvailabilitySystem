#base image
FROM python:3.6.5-alpine

# set working directory
WORKDIR /usr/src/app

# copy and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app

RUN python manage.py recreate-db

# run server
CMD ["/usr/src/app/entrypoint.sh"]
