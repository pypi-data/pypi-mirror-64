# Starlette OAuth2

A Startlette middleware for authentication through oauth2's authorization code grant type, which is often used to add authentication and authorization to a web application that interacts with an API.

This middleware is intented to be used when the application relies on an external tenant (e.g. Microsoft AD) for authentication.

Check `example/` for a concrete implementation.

## How to run the example against Microsoft AD

Note: the values in capital such as `CLIENT_ID` are to be replaced in `example/.venv`.

1. Generate a secret and write its value on `SECRET_KEY`

2. Go to Azure AD, create an app registration (`app registrations`), give it a name, and add `http://localhost:5001/authorized` as a `Redirect URI`.
    * replace the value on `CLIENT_ID` by the value on `Application (client) ID`
    * replace the value on `TENANT_ID` by the value on `Directory (tenant) ID`

3. In `Certificates & secrets`, create a new client secret.
    * replace the value on `CLIENT_SECRET` by the value of the key you just created under `Client secrets`

4. Install dependencies and run:

```
cd examples
python -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python -m app
```

When you visit `http://localhost:5001/public`, you will see that you are not authenticated.
When you visit `http://localhost:5001`, you will be redirected to your tenant, to authenticate. Once authenticated, you will be redirected back to `http://localhost:5001`, and your email will appear.

Public endpoints are optional. They are useful for e.g. health checks.
