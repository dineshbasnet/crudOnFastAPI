from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is started...")
    await init_db()
    yield
    print(f"server has been stopped")
        
    

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    lifespan=life_span
)

app.include_router(book_router,prefix="/books",tags = ['books'])
app.include_router(auth_router,prefix="/auth",tags=['users'])