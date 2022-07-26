# Webcamphoto-sharer

Create an account on https://cloud.google.com/ .

Select or create a new project. 

Go top left to navigation menu and select APIs & Services -> Library -> Type 'photos' in the checkbox -> Enable . 

After API is enabled, go to Credentials -> Configure consent screen.

User Type: External -> Create. 

On OAuth consent screen complete * text boxes.
After, select upload scopes because we will only upload photos to our account, then add a test user to let. ( See, upload, and organize items in your Google Photos library  )
Go to Credentials after completion and then click on + CREATE CREDENTIALS. Select OAuth client ID, because Google Photos API only works with OAuth client ID, not with an API Key.
Select Desktop app and give a name. Click on donwload JSON and rename it: e.g: client_secret_Webcam-Sharer.json . Copy to your project folder.
Rename CLIENT_SECRET_FILE = 'c_secret.json' (init_photo.py) to your filename. You can edit SCOPES (e.g manipulate media items from Google Photos ).
Run the app. Then it should open a browser and redirect you to accounts.google.com and it will print a link in console: 'Please visit this URL to authorize this application:'.
Select your test account and then it should plot 'The authentication flow has completed. You may close this window.'
Run the app, it should start and in console you should see: 'photoslibrary service created successfully'.
If you have Unable to open device "/dev/input/event6". Please ensure you have the appropriate permissions. -> sudo chmod 755 /dev/input/event6 in terminal.

Requirements: 
pip3 install google
pip3 install kivi
pip3 install requests
pip3 install oauth2client
