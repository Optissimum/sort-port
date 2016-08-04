# Sort-Port - A simple group inventory tracker


## Feature Support
 * Python 2


## Installation
  From within the Sort-Port folder, open a python console and run
  ```
from app import database
database.create_all()
  ```

  Also be sure to enable http-approved login with
  ```
  export OAUTHLIB_INSECURE_TRANSPORT=1
export OAUTHLIB_RELAX_TOKEN_SCOPE=1
  ```
  on your console

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
