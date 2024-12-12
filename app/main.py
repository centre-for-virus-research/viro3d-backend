from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.routes import (
genome_coordinates,
health_check,
proteins,
viruses,
zip
)
from app.utils.env_variables import *
from app.routes.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(
    root_path="/api",
    version='1.0',
    title='Viro3D',
    description='Viro3D is an API for retrieving metatadata and structural models of AI-enabled predicted protein structures. If you experience any browser slow-down, please use the <page_size> and <page_num> fields when making requests to limit the number of responses.',
)

app.include_router(health_check.router)
app.include_router(proteins.router)
app.include_router(viruses.router)
app.include_router(genome_coordinates.router)
app.include_router(zip.router)
app.mount("/pdb", StaticFiles(directory=Path(STRUCTURAL_MODELS_PATH)))
app.mount("/graph_data", StaticFiles(directory=Path(GRAPH_DATA_PATH)))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)