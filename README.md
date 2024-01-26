# youtube-auto-playlist
This script automates adding videos to a personal playlist by matching keywords in the original playlist.

## Installing Dependencies
`pip install google-api-python-client` \
`pip install --upgrade google-api-python-client google-auth-oauthlib google-auth-httplib2`

## Set-up and credentials
1.Create or select a project in the [API Console](https://console.cloud.google.com/) 

2.In the [library panel](https://console.developers.google.com/apis/library), search for the YouTube Data 
API v3. Click into the listing for that API and make sure the API is enabled for your project.\

3.In the [credentials panel](https://console.developers.google.com/apis/credentials), create two credentials:

  * Create an API key. You will use the API key to make requests that do not require user     
  authorization.

  * Create an OAuth 2.0 client ID and set the application type to Other. You will need OAuth 2.0       
  credentials for requests that require user authorization.
  
  * copy the the API key.\
  `echo 'export YT_API_KEY="YOUR_API_KEY"' >> ~/.bashrc ` 
  `source ~/.bashrc`

  * Download the JSON file that contains your OAuth 2.0 credentials and rename it as `credentials.json`.
  Move the file to this repository.

## Note
  * OAuth Consent screen might require additional permissions and the redirect URI, which can be added in the appropriate Client ID
   details.

## Run 

Once the credentials.json is in path, Run `python3 main.py`

  

