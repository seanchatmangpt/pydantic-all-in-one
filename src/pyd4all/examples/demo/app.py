from __future__ import annotations as _annotations

import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastui import prebuilt_html
from fastui.auth import fastapi_auth_exception_handling
from fastui.dev import dev_fastapi_app
from httpx import AsyncClient

from pyd4all.examples.demo.auth import router as auth_router
from pyd4all.examples.demo.components_list import router as components_router
from pyd4all.examples.demo.forms import router as forms_router
from pyd4all.examples.demo.sse import router as sse_router
from pyd4all.examples.demo.tables import router as table_router
from pyd4all.utils.routing_tools import load_filesystem_routes


@asynccontextmanager
async def lifespan(app_: FastAPI):
    async with AsyncClient() as client:
        app_.state.httpx_client = client
        yield


frontend_reload = '--reload' in sys.argv
if frontend_reload:
    # dev_fastapi_app reloads in the browser when the Python source changes
    app = dev_fastapi_app(lifespan=lifespan)
else:
    app = FastAPI(lifespan=lifespan)

fastapi_auth_exception_handling(app)
app.include_router(components_router, prefix='/api/components')
app.include_router(sse_router, prefix='/api/components')
app.include_router(table_router, prefix='/api/table')
app.include_router(forms_router, prefix='/api/forms')
app.include_router(auth_router, prefix='/api/auth')
# app.include_router(main_router, prefix='/api')


@app.get('/robots.txt', response_class=PlainTextResponse)
async def robots_txt() -> str:
    return 'User-agent: *\nAllow: /'


@app.get('/favicon.ico', status_code=404, response_class=PlainTextResponse)
async def favicon_ico() -> str:
    return 'page not found'


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))


def main():
    """Main function"""
    from dslmodel import init_lm, init_instant, init_text
    init_instant()
    load_filesystem_routes(app, "fastapi", config_path="watcher_config.yaml")

    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == '__main__':
    main()
