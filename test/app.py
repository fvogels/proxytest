from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


app = FastAPI()


@app.get('/')
async def index(request: Request):
    return {
        'foo': str(request.url_for('foo'))
    }



@app.get('/foo')
async def foo():
    return 'foo'