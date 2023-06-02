from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id: int 
    title: str 
    author: str
    description: str 
    rating: int 
    published_date: int 

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date



class BookRequest(BaseModel):
    id: Optional[int] = Field(title="Not Required")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt= -1, lt=6)
    published_date: Optional[int] = Field(gt=1999, lt=2031)

    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'codingwithruby',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 2029
        }
    }

BOOKS = [
    Book(1, "Computer Science Pro", "codingwithruby", "A very nice book", 5, 2021),
    Book(2, "FastApi Pro", "codingwithruby", "A great book", 3, 2018),
    Book(3, "Endpoint Pro", "Author 1", "A awesome book", 4, 2022),
    Book(4, "Java 101", "Author 2", "test 2", 10, 2025),
    Book(5, "Python 101", "Author 3", "test 1", 2, 2000)
]

@app.get("/books")
async def get_book():
    return BOOKS 

@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    rating_book = []
    for book in BOOKS:
        if book.rating == book_rating:
            rating_book.append(book)

    return rating_book 

@app.get("/books/published_book/")
async def read_book_by_published_date(published_date: int):
    published_book = []
    for book in BOOKS:
        if book.published_date == published_date:
            published_book.append(book)
    
    return published_book

@app.post("/create_book")
async def new_book(book_request: BookRequest):
    new_book1 = Book(**book_request)
    BOOKS.append(find_book_id(new_book1))

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book

@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    
    raise HTTPException(status_code=404, detail="Item not found")
        

@app.put("/books/update_book/")
async def update_book(book_update: BookRequest):
    for book in BOOKS:
        if book.id == book_update.id:
            book = book_update

@app.delete("books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS[i].pop()