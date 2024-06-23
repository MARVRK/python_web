from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis
import logging
from starlette.responses import JSONResponse

from api.core.config import settings
from api.endpoints import auth, contacts, users

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log"),  # Log to a file
    ],
)

logger = logging.getLogger("myapp")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred"},
    )

app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(contacts.router, prefix="/api", tags=["contacts"])
app.include_router(users.router, prefix="/api", tags=["users"])

@app.on_event("startup")
async def startup():
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
