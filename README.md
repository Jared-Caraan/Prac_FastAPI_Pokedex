# FastAPI

## Quick Notes
1. `async` is not needed in FastAPI, it can be done behind the scenes 
if necessary.
2. Order matters with Path Parameters
3. You can use Query Parameters with Path Parameter

## Status Codes:
1. 1xx - Information Response: Request Processing.
2. 2xx - Success: Request Successfully Complete.
3. 3xx - Redirection: Further action must be complete.
4. 4xx - Client Errors: An error was caused by the client.
5. 5xx - Server Errors: An error occurred on the server.

### Successful Status Codes:
200: OK - Standard Response for a Successful Request. Commonly used for successful Get request 
            when data is being returned.
201: Created - The request has been successful, creating a new resource. Used when a POST creates an entity.
204: No Content - The request has been successful, did not create an entity nor return anything. 
            Commonly used with PUT requests.

### Client Errors Status Codes:
400: Bad Request - Cannot process request due to client error. Commonly used for invalid request methods.
401: Unauthorized - Client does not have valid authentication for target resource.
404: Not Found - The clients requested resource can not be found.
422: Unprocessable Entity - Semantic errors in Client Request.

### Server Status Codes:
500: Internal Server Error - Generic Error Message, when an unexpected issue on the server happened.
