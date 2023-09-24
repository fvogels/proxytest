from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from typing import List, Tuple
from starlette.types import ASGIApp, Receive, Scope, Send

Headers = List[Tuple[bytes, bytes]]

class ProxiedHeadersMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope["headers"] = self.remap_headers(scope.get("headers", {}))

        await self.app(scope, receive, send)
        return

    def remap_headers(self, source: Headers) -> Headers:
        """
        Map X-Forwarded-Host to host and X-Forwarded-Prefix to prefix.

        """

        source = dict(source)

        if b'x-forwarded-host' in source:
            source.update({b'host': source[b'x-forwarded-host']})
            source.pop(b'x-forwarded-host')

        if b'x-forwarded-prefix' in source:
            source.update({
                b'host': source[b'host'] + source[b'x-forwarded-prefix']
            })
            source.pop(b'x-forwarded-prefix')

        source = [(k, v) for k, v in source.items()]

        return source


app = FastAPI()
app.add_middleware(ProxiedHeadersMiddleware)


@app.get('/')
async def index(request: Request):
    return {
        'foo': str(request.url_for('foo'))
    }



@app.get('/foo')
async def foo():
    return 'foo'