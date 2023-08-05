# aiohttp_google_auth_backend
The Google Authentication Library for python, 
[google-auth](https://google-auth.readthedocs.io/en/latest/index.html),
provides **verify_token** (and verify_oauth2_token) methods, which can be used by
backend servers to verify the token provided by the 
web/mobile application and return decoded profile fields. However, python google-auth does
not yet provide the support for asyncio.

The **aiohttp_google_auth_backend** library provides async
wrapper for these methods.
    
# How to use it

aiohttp_google_auth_backend package provides JSAioGoogleTokenVerifier class to asynchronously handle the token verification.

The library uses the asynchronous task to fetch and cache the 
GOOGLE OAUTH2 Certificates in the background using aiohttp Client API.
* Create an instance of JSAioGoogleTokenVerifier, along with the aiohttp web application instance, during the startup.
* Register **on_startup** method of the instance with on_startup of web application to fetch the certificates for first rime and then start the background thread to re-fetch the certificates.
* Register **on_cleanup** method of the instance with on_cleanup of web application to cancel the background thread when the process is being stopped.
* Constructor for the JSAioGoogleTokenVerifier class provides following parameters to customize re-fetching of certificates.
    * By default, library uses the "Expires" header to identify when the certificates need to be re-fetched.
        * The *ok_renew_interval* parameter can be used to specify interval to re-fetch certificates (e.g. every hour).
    * If the library fails to fetch the certificates, it will repeatedly try to re-fetch certificates until successful.
        * Library starts with initial delay of *min_error_renew_interval* (default: 1 second) and
         exponentially backoff the interval for each sub-sequent fetch till the delay reaches **max_error_renew_interval**.
    * Token fields to be returned are identified by parameter **profile_fields** (default: email)
         
Following code sample assume that token to be verified is passed as parameter idtoken. 

```python
from aiohttp import web
from aiohttp_google_auth_backend import JSAioGoogleTokenVerifier

SAMPLE_GOOGLE_CLIENT_ID = "YOUR GOOGLE APPID"


async def handleLogin(request):
    data = await request.json()
    status, res = await request.app['verifyGoogleToken'].verify_token(data["idtoken"], SAMPLE_GOOGLE_CLIENT_ID)
    if status == 200:
        return web.json_response(res, status=status)
    else:
        return web.json_response(dict( error=str(res['error'])), status=status)


async def app_startup(app):
    app['JSAioGoogleTokenVerifier'] = JSAioGoogleTokenVerifier()
    await app['JSAioGoogleTokenVerifier'].on_startup()


async def app_cleanup(app):
    await app['JSAioGoogleTokenVerifier'].on_cleanup()


def app_run():
    app = web.Application()
    app.on_startup.append(app_startup)
    app.on_cleanup.append(app_cleanup)
    app.add_routes([web.post('/login', handleLogin)])
    web.run_app(app)


if __name__ == '__main__':
    app_run()
```

 
