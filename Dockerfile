#ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh
FROM ubuntu
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh
RUN cat  /home/netfree-unix-ca.sh | sh
RUN chmod +x /home/netfree-unix-ca.sh
# install app dependencies

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install pytest
RUN pip install requests
RUN pip install pytest-parallel
RUN pip install psutil

# copy twtask and test
COPY . . 


# final configuration 
CMD pytest test_get_from_different_pages.py --workers 8
