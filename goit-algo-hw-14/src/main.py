from pathlib import Path

import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes import contacts, auth, users
from src.conf.config import config

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")

@app.on_event("startup")
async def startup():
    """
    This function is an event handler that runs when the FastAPI application starts.
    It initializes a Redis connection and sets up the FastAPILimiter with the Redis instance.

    Parameters:
    None

    Returns:
    None

    Raises:
    HTTPException: If there is an error initializing the Redis connection.
    """
    try:
        print("Initializing Redis connection...")
        r = redis.Redis(
            host="redis",
            port=config.REDIS_PORT,
            db=0,
            decode_responses=True
        )
        await r.ping()  # Test the connection to Redis
        await FastAPILimiter.init(r)
        print("Redis initialized successfully.")
    except Exception as e:
        print(f"Error initializing Redis: {e}")
        raise HTTPException(status_code=500, detail="Redis initialization failed")

templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """
    This function serves as the root endpoint of the FastAPI application.
    It renders the "index.html" template from the "templates" directory using Jinja2.

    Parameters:
    request (Request): The FastAPI Request object containing information about the incoming request.

    Returns:
    TemplateResponse: A FastAPI response object with the rendered "index.html" template.

    Raises:
    None
    """
    return templates.TemplateResponse(
        "index.html", {"request": request, "our": "MARVRK-Test-HM13"}
    )

@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    This function serves as a health check endpoint for the FastAPI application.
    It connects to the database and executes a simple SELECT query to verify the connection.

    Parameters:
    db (AsyncSession): An asynchronous database session provided by the FastAPI dependency injection system.
                       The default value is obtained from the 'get_db' function.

    Returns:
    dict: A dictionary containing a 'message' key with the value "Welcome to FastAPI!".
          If the database connection fails, an HTTPException is raised with a 500 status code and a
          'detail' key with the value "Error connecting to the database".

    Raises:
    HTTPException: If there is an error connecting to the database.
    """
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database")
