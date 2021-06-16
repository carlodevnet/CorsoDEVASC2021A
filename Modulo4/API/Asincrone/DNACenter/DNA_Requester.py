# Author: Stefano Pilla 

# Descrizione: Questo codice è stato creato per la dimostrazione delle API Asincrone
# Utilizza la DevNet Sandbox (DNA Center) raggiungibile a questo indirizzo:
# https://developer.cisco.com

import requests
import time
import json

# Let's define an helper class with all the methods
class DNACRequester:
    
    # Main constructor to create a new DNA Object
    def __init__(self, host, username, password, verify=True, old_style=False):

        # Host is the hostname/IP and verify is for SSL Cert verification
        self.host = host
        self.verify = verify

        # Disable Warnings 
        if not verify:
            requests.packages.urllib3.disable_warnings()
        
        # Build common headers that will be used for all the requests
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Check if it's an old version of DNA and change the URL accordingly
        # There are 2 version of DNA center APIs
        if old_style:
            auth_url = "api/system/api/v1/auth/token"
        else:
            auth_url = "dna/system/api/v1/auth/token"

        # Capture the response to the Authentication request
        # For DNA we need to get an X-Auth-Token before perform any actions
        auth_resp = self._req(resource=auth_url, method="post",
                              auth=(username, password))

        # Uncomment only for troubleshooting in case of issues
        # print(auth_resp.text)

        # Check if the response is a 4xx or 5xx and in case raise an exception
        auth_resp.raise_for_status()
        
        # In case the request has not raised any exception get the X-Auth-Token from
        # the response
        self.headers['X-Auth-Token'] = auth_resp.json()['Token']

        # Uncomment only for troubleshooting in case of issues
        # print(self.headers)

    # Define a method for all the requests
    # By default it will be a GET with no params, auth o anything else set
    def _req(self, resource, method="get", auth=None, jsonbody=None, params=None, raise_for_status=True, verify=False):

        # Uncomment only for troubleshooting in case of issues
        # print(f"https://{self.host}/{resource}")

        # Issue a generic request based on the value received as arguments
        resp = requests.request(
            method=method, url=f"https://{self.host}/{resource}", auth=auth, headers=self.headers, json=jsonbody, params=params, verify=verify)

        # Uncomment only for troubleshooting in case of issues
        # print(resp.text)

        # Check if the raise_for_status variable == True 
        # which means that there was a 4xx o 5xx error so raise an exception
        # Otherwise return the response 
        if raise_for_status:
            resp.raise_for_status()
        return resp

    # Define a method to manage the Aynchrounous API
    # By default this method will check every 5 seconds for 3 times
    # but this behaviour could be changed passing the wait_time and attemps arguments
    def _wait_for_task(self, task_id, wait_time=15, attempts=20):

        # Wait until the task is complete making the API call synchronous
        # Iterate until the attempts variable and wait "wait_time" seconds
        for _ in range(attempts):
            time.sleep(wait_time)

            # Query DNA center with the task ID. This task is passed as argument to this function
            task_resp = self._req(f"dna/intent/api/v1/task/{task_id}")
            
            # Convert the response into a json object and get the value of the "response" key
            task_data = task_resp.json()['response']

            # Uncomment in case of issues for troubleshooting
            print(json.dumps(task_data, indent=2))

            # If an error occured the isError will be set to True by DNA
            # in this case, rais an exception and get the reason
            if task_data['isError']:
                reason = task_data.get("failureReason", task_data['progress'])
                raise ValueError(f"Asynch task error: {reason}")

            # if isError is false, there's no error but we might not be done yet 
            # so we check until endTime is present in the response and only when 
            # we find a value we return the task_resp to be inspected in details
            if "endTime" in task_data:
                return task_resp
                
        # if isError is false but we are not done yet (no endTime value in the response) keep looping
        # until the max attempts. After the attempts reach the max value then timeout the request        
        total = wait_time * attempts
        raise TimeoutError(f"Task timed out in {total} seconds")
