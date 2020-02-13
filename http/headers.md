



# CORS

Preflight request for Methods with side-effects (POST, DELETE, etc)
 * sends an OPTIONS request

## Regex Responses

nginx can check the origin for "allowed" sites

1. match on the Origin Header
2. Set CORS headers for the origin if it passes

However these requests might be cached?

 * See the "Vary: Origin" header, which disables caching
 * https://www.w3.org/TR/cors/#resource-implementation


```apache
SetEnvIf Origin ^(https?://.+\.mywebsite\.com(?::\d{1,5})?)$   CORS_ALLOW_ORIGIN=$1
Header append Access-Control-Allow-Origin  %{CORS_ALLOW_ORIGIN}e   env=CORS_ALLOW_ORIGIN
Header merge  Vary "Origin"
```
