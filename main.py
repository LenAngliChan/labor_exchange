from fastapi import FastAPI
from src.routers import user_router, job_router, response_router, auth_router
from src.settings import db_init
import uvicorn
from src.core.config import STAGE

app = FastAPI()
app.include_router(user_router)
app.include_router(job_router)
app.include_router(response_router)
app.include_router(auth_router)

if STAGE == 'memory':
    try:
        db_init()
    finally:
        pass


@app.get("/")
async def hello():
    return {"message": "Hello, Daniel!"}


if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)
