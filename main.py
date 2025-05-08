from fastapi import FastAPI
from database import Base, engine
from routers import books, ws

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(books.router, prefix="/mylib", tags=["Books"])
app.include_router(ws.ws_router)
