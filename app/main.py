from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
health_check,
proteins,
viruses
)

app = FastAPI(
    root_path="/api",
    version='1.0',
    title='Viro3D',
    description='Viro3D is an API for retrieving metatadata and structural models of AI-enabled predicted protein structures.',
)

app.include_router(health_check.router)
app.include_router(proteins.router)
app.include_router(viruses.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)