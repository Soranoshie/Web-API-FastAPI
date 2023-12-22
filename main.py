from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import event_model, user_model
from db_context import engine
from router import router_websocket, router_events, router_users

event_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)


templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="WebAPIPractice3",
    summary="Get user data",
    version="0.0.1",
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_urn = request.url.netloc
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol,
                                       "server_urn": server_urn})


app.include_router(router_websocket)
app.include_router(router_events)
app.include_router(router_users)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
