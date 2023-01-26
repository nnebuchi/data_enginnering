FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

# this path will be created in the container and the entire content will be in it
WORKDIR /app

# copy file from local machine into docker container
COPY injest_data.py injest_data.py

ENTRYPOINT [ "python", "injest_data.py"]