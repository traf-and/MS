from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import uvicorn
from sqlalchemy import create_engine

from app import module
# import module

app = FastAPI()

# connect/createDB
engine = create_engine('sqlite:////app/data/short_URL.db', echo=True)
# engine = create_engine('sqlite:///short_URL.db', echo=False)
conn = engine.connect()
# create table if not exists
module.create_table(engine)

# a. POST /shorten: Принимает полный URL (JSON: {"url":"..."}) и возвращает короткую ссылку.
# b. GET /{short_id}: Перенаправляет на полный URL, если он существует.
# c. GET /stats/{short_id}: Возвращает JSON с информацией о полномURL.

@app.post('/shorten', summary='Create short URL', response_model=module.ShortURL)
async def shorten(url:module.URL)->module.ShortURL:
    short_url = url.create_short_id(conn)
    return short_url

@app.get('/stats/short_id', summary='Get info about URL')
async def url_info(short_url:str)->module.URLInfo:
    print(short_url)
    short_url = module.ShortURL(short_url=short_url)
    url_info = module.URLInfo()
    url_info = url_info.info_by_short(short_url, conn)
    return url_info

@app.get('/{short_id:path}', summary='Redirect to full url', response_class=RedirectResponse)
async def redirect_by_short(request:Request)->str:
    short_url = module.ShortURL(short_url=request.url.path[1:])
    url = short_url.get_full_url(conn)
    return RedirectResponse(url=url.url)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=10000, reload=True, log_level="debug",
                workers=2)