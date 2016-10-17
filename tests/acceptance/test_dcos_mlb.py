import time
import requests
from shakedown import *

MLB_PACKAGE_NAME = 'marathon-lb'
EXTERNAL_LB = ''
# EXTERNAL_LB is for environments where another LB sits in front of MLB such as an AWS Public ELB
# Format is 'thomas-kr-publicsl-2qzq6zn0gq3l-460803782.us-east-1.elb.amazonaws.com'
# Leave EXTERNAL_LB ='' in environments where the Public IP of Public Agent is exposed externally and can be reached by maching running the test.

def test_check_mlb():
    package_status = package_installed(MLB_PACKAGE_NAME)
    assert package_status is True
    if package_status == True:
            print(MLB_PACKAGE_NAME + ' is installed.')

def test_get_public_agents():
    public_agents = get_public_agents()
    assert isinstance(public_agents, list)
    print("Public Agents are " + str(public_agents))
    return public_agents

def test_mlb_connection():
    public_agents = get_public_agents()
    assert isinstance(public_agents, list)
    if (EXTERNAL_LB == ''):
        public_agent = str(public_agents[0])
    else:
        public_agent = EXTERNAL_LB
    print("Public Hostname or Address to test MLB = " + public_agent)
    response = requests.get('http://'+ public_agent +':9090/haproxy?stats')
    if response.status_code == 200:
        print("Response from MLB is " + str(response.status_code) +" Marathon-lb is installed on the cluster.")
    else:
        print("Response from MLB is" + str(response.status_code) +" is ERROR response from MLB..")
        assert response.status_code is 200
