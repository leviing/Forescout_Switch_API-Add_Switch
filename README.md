# Forescout_Switch_API-Add_Switch

This Python script leverages the Forescout Switch API to add a list of switches, in a .csv, to the Forescout Switch plugin.

The script starts by prompting the terminal for required info:

- API username
- API password
- IP address of the Forescout Enterprise Manager (EM)
- The CSV file containing the list of switches
- IP address of the Managing Forescout Appliance for the new switch
- Switch profile to apply to the new switch

After receiving the input, the script will then open the CSV and loop through each address in the list. It performs the following for each switch address in the list:

- An authentication token is requested from the EM using the username/password provided. That auth token is then provided back in the header of the HTTP POST that also contains the payload to add the switch to the plugin.
- If an HTTP 200 OK response is received a success message is printed to the terminal.
- If the response is not an HTTP 200 OK response, then a failure message is printed to the terminal. 
