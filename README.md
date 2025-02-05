# Tinkerfolio LMS Backend

Forked from [Echoclass](https://echoclass.com) by [Michael Chen](https://github.com/michaelchen-lab).

## Implementation Details

- PostgreSQL is used. For static file storage, AWS S3 is chosen.
- The SQL database schema can be found in files _accounts/models.py_ and _core/models.py_
- JWT token is the chosen authentication method.
- This app has been setup to handle WebSocket connections. Daphne is used as the ASGI server.

## More Information

For more details on the implementation, please refer to the [docs](https://github.com/tinkertanker/LMS_Frontend/blob/main/documentation/DeveloperGuide.md).

The frontend of this project can be found [here](https://github.com/tinkertanker/tinkerfolio-lms-frontend).
