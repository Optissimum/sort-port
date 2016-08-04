# Sort-Port - A simple group inventory tracker


## Setup, Installation, and Use
  From within the Sort-Port folder, open a python console and run
  ```
from app import database
database.create_all()
  ```

  Enable http-approved login on your console
  ```
  export OAUTHLIB_INSECURE_TRANSPORT=1
export OAUTHLIB_RELAX_TOKEN_SCOPE=1
  ```
  
  Last but not least, enter your secret key and google id login id/secret into secrets.py 
  
  To use the application in debug mode, run ```python run.py``` in the sort-port folder

## Requirements
 * Python 2
 * bleach
 * blinker
 * click
 * Flask
 * Flask-Dance
 * Flask-Login
 * Flask-SQLAlchemy
 * Flask-WTF
 * html5lib
 * httplib2
 * itsdangerous
 * Jinja2
 * lazy
 * MarkupSafe
 * oauth2client
 * oauthlib
 * pkg-resources
 * pyasn1
 * pyasn1-modules
 * requests
 * requests-oauthlib
 * rsa
 * six
 * SQLAlchemy
 * SQLAlchemy-Utils
 * URLObject
 * Werkzeug
 * WTForms
