FROM ubuntu
# install app dependencies

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install pytest
RUN pip install requests
RUN pip install pytest-parallel
RUN pip install psutil

# copy twtask and test
COPY . . 


# final configuration 
#CMD pytest test_get_from_different_pages.py --workers 8
CMD pytest tests.py
