from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cicd_router

app = FastAPI(title="Project 20: CI/CD Pipeline API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(cicd_router.router)

@app.get("/")
def read_root():
    return {"message": "Project 20 CI/CD Automation Backend is online!"}