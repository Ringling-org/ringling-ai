from fastapi import FastAPI
from api import summary

app = FastAPI()

BASE_URL = "/api"

def register_router(app: FastAPI, module):
    if not hasattr(module, "router"):
        raise RuntimeError(f"❌ '{module.__name__}' 모듈에 'router'가 없습니다.")
    if not hasattr(module, "ROUTE_PREFIX"):
        raise RuntimeError(f"❌ '{module.__name__}' 모듈에 'ROUTE_PREFIX'가 없습니다.")

    app.include_router(module.router, prefix=BASE_URL + module.ROUTE_PREFIX)

register_router(app, summary)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)