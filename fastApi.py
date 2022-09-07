import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from main import get_database

app = FastAPI()


@app.get('/events')
async def events():
    value_list = []
    for value in await get_database():
        value_list.append(json.loads(value))
    return JSONResponse(value_list)
