# LMS Backend
Co-developed with TinkerTanker

## Database & Storage

PostgreSQL is used. For static file storage, AWS S3 is chosen. 

The SQL database schema can be found in files *accounts/models.py* and *core/models.py* 

## Accounts

JWT is the chosen authentication method. This Django app consists of 3 auth-related endpoints:

1. *token/* - Takes in username and password. If valid, an access and refresh token is sent to client.
2. *token/refresh/* - Takes in refresh token. If valid, a new access token is created and sent to client.
3. *token/verify/* - Takes in access token. If valid, a 200 status code will be sent to client.

## Core

The core Django app handles the LMS's main functionalities. Currently, there are 2 main groups of endpoints, which correspond to our DB models.

1. *Classroom* - Available actions: List, Retrieve, Create, Update
2. *StudentProfile* - Available actions: List, Update

This app has been setup to handle WebSocket connections. The specific endpoints will be added in the next milestone.
