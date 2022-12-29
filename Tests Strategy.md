
Tests Strategy.

Scope: 
The tests are testing a web server that includes a database of players. 
The API returns a simple JSON body that contains IDs and names of players. 
The API requires Basic authentication. 
Currently, the only supported username and password pair is admin/admin.     

Approach: 

Functional tests – get IDs and names of players, get correct status code for get requests.
Negative tests- access invalid page number, delete or post methods. 
Reliability tests – The data from the server is not changed for each get. 
Short security tests – server not allowed to login without username and password, and server should reject a client after a few wrong attempts – TBD.
Performance tests – CPU, Memory.
Stress tests, Load tests 

Environment: 
The server runs on Linux, the tests are written in python.   

Tool: 
Pytest framework is used for the tests   

Release:
N\A 
  
Risk:
The server has some bugs...
