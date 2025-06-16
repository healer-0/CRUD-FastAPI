from fastapi import FastAPI,Depends,HTTPException
from . import services, schemas
from .db import engine,SessionLocal
from .models import Base
from sqlalchemy.orm import Session
import sentry_sdk
from dotenv import load_dotenv
import os

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_URL"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)


Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

@app.get('/books/', response_model=list[schemas.Book])
def get_all_books(db:Session=Depends(get_db)):
    return services.get_books(db)

@app.get('/books/{id}', response_model=schemas.Book)
def get_book_by_id(id:int,db:Session=Depends(get_db)):
    book_queryset= services.get_book(db, id)
    if book_queryset:
        return book_queryset
    raise HTTPException(status_code=404,detail="Invalid book id")

@app.post('/books/', response_model=schemas.Book)
def create_new_book(book: schemas.BookCreate, db:Session=Depends(get_db)):
    return services.create_book(db, book)

@app.put('/books/{id}', response_model=schemas.Book)
def update_book(book: schemas.BookCreate, id:int, db:Session=Depends(get_db)):
    db_update= services.update_book(db, book, id)
    if not db_update:
        raise HTTPException(status_code=404,detail="Book Not Found")
    return db_update

@app.delete('/books/{id}', response_model=schemas.Book)
def delete_book(id:int,db:Session=Depends(get_db)):
    delete_entry= services.delete_book(db, id)
    if delete_entry:
        return delete_entry
    raise HTTPException(status_code=404,detail="Book not Found")