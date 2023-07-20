# LMS Backend
Co-developed with Tinkertanker

## Implementation Details

- PostgreSQL is used. For static file storage, AWS S3 is chosen. 
- The SQL database schema can be found in files *accounts/models.py* and *core/models.py* 
- JWT token is the chosen authentication method.
- This app has been setup to handle WebSocket connections. Daphne is used as the ASGI server.

## More Information
For more details on the implementation, please refer to the [docs](docs/docs.md).

The frontend of this project can be found [here](https://github.com/tinkertanker/LMS_Frontend).
