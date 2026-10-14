from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.timetable import router as timetable_router
from app.api.crud import router as crud_router

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(timetable_router, prefix="/api/timetable", tags=["timetable"])
app.include_router(crud_router, prefix="/api", tags=["crud"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Timetable Generator API"}
