import requests
import urllib3
import json
import csv
import getpass

# inhibit self-signed certificate warnings
urllib3.disable_warnings()

# function that reaches out to the switch api to receive the authentication token required for main function
def getAuth(apiUser, apiPass, fsEM):

    # base url for auth token request
    url = "https://"+fsEM+"/fsum/oauth2.0/token"
    
    # payload and header for auth token request
    payload='username='+apiUser+'&password='+apiPass+'&grant_type=password&client_id=fs-oauth-client'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    # auth token request and response saved as variable
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    # convert response to json
    response_json = response.json()

    # parse the auth token from the response
    token = response_json['access_token']
    
    # return the auth token to calling point
    return token
    
    
def main():
    
    # retrieve the SW API username, SW API password (secure), ForeScout EM, CSV with list of devices, FS appliance managing the switch, and switch profile from the user input
    apiUser = input('API Username: ')
    apiPass = getpass.getpass('API Password: ')
    fsEM = input('ForeScout EM IP Address: ')
    deviceCSV = input('CSV list of devices: ')
    fsAppliance = input('FS Management Appliance IP Address: ')
    switchProfile = input('Switch Profile to apply: ')
    
    # open the CSV containing the network device addresses
    with open(deviceCSV, newline='') as csvfile:
    
        #read the CSV into a list
        switches = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
        # loop through rows in the list
        for row in switches:
        
            # parse the ip address from the row
            switch = ', '.join(row)
            
            # get the auth token from the SW API
            token = getAuth(apiUser, apiPass, fsEM)
            
            # base url for switch plugin
            url = "https://"+ fsEM +"/switch/api/v1/switches"

            # payload for request to add switches to the plugin by profile
            payload = json.dumps({
              "switchToAddList": [
                {
                  "comment": "Add via SW API",
                  "connectingAppliance": fsAppliance,
                  "managementAddress": switch,
                  "profileName": switchProfile
                }
              ]
            })

            # header for request to add switches to the plugin by profile
            headers = {
              'Authorization': 'Bearer '+ token,
              'Content-Type': 'application/json'
            }

            # switch add request with response stored in variable
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            
            # print status message for each entry. 200 is good, 4xx is bad
            if str(response) == '<Response [200]>':
                print('Successfully added '+ switch +', managed by '+ fsAppliance +', to the '+ switchProfile +' profile.'+ str(response))
            else:
                print('Failed to add '+ switch +' to switch plugin.'+ str(response))


if __name__ == '__main__':
    main()