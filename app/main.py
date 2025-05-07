from fastapi import FastAPI
from api import ping_test

URL_PREFIX = "/api"
app = FastAPI()

app.include_router(ping_test.router, prefix=URL_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)