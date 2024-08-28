
# API Test Harness
import requests
import uuid 

# Making a PUT request
r = requests.get('http://localhost:8802/moodle-badges-for-user/2')
 
# check status code for response received
# success code - 200
print(r)
 
# print content of request
print(r.content)
