from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.api_routes import router as api_router
import uvicorn

app = FastAPI()

app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False, workers=10)