from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from . import accounts
from . import auth
from . import shops
from . import transactions
from .config import settings


app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie='session',
    max_age=1000000
)
accounts.initialize_app(app)
auth.initialize_app(app)
shops.initialize_app(app)
transactions.initialize_app(app)
