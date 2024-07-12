from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints.weather import router as weather_router
from endpoints.info import router as info_router

app = FastAPI()
app.include_router(weather_router)
app.include_router(info_router)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)