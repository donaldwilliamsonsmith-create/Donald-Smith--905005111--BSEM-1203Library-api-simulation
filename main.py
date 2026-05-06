from fastapi import FastAPI, HTTPException
import asyncio
from typing import Dict

app = FastAPI()

# Fake database
books: Dict[int, dict] = {
    1: {"title": "Python Basics", "available": True},
    2: {"title": "API Design", "available": True},
    3: {"title": "Data Communication", "available": True},
}

# GET all books
@app.get("/books")
async def get_books():
    return books

# Borrow book
@app.post("/borrow/{book_id}")
async def borrow_book(book_id: int):
    await asyncio.sleep(1)  # simulate delay

    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")

    if not books[book_id]["available"]:
        raise HTTPException(status_code=400, detail="Book already borrowed")

    books[book_id]["available"] = False
    return {"message": f"You borrowed {books[book_id]['title']}"}

# Return book
@app.post("/return/{book_id}")
async def return_book(book_id: int):
    await asyncio.sleep(1)  # simulate delay

    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")

    books[book_id]["available"] = True
    return {"message": f"You returned {books[book_id]['title']}"}

# Simulate multiple users borrowing at once
@app.get("/simulate")
async def simulate_users():
    async def user_action(book_id):
        return await borrow_book(book_id)

    results = await asyncio.gather(
        user_action(1),
        user_action(2),
        return_exceptions=True
    )

    return {"simulation": results}