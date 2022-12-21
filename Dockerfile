FROM ubuntu:18.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install pytest
RUN pip install requests


# copy twtask and test
COPY twtask .
COPY test.py .

# final configuration
CMD pytest -s
