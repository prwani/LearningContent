"""Simple demo MCP server for library management operations.

This server provides book catalog management, member management,
and lending/borrowing operations for a library system.
"""

import random
from datetime import datetime, timezone
import os
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field
from rich import print

mcp = FastMCP(
    name="Library Management MCP Server",
)


@mcp.tool(name="add_book", description="Add a new book to the library catalog.")
def add_book(
    title: Annotated[str, Field(description="Title of the book")],
    author: Annotated[str, Field(description="Author of the book")],
    isbn: Annotated[str, Field(description="ISBN number")],
    year: Annotated[int, Field(description="Publication year")],
) -> dict:
    print(f"[green]invoking tool:add_book title={title}, author={author}[/green]")
    return {
        "status": "added",
        "book_id": "book_12345",
        "title": title,
        "author": author,
        "isbn": isbn,
        "year": year,
        "added_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(name="delete_book", description="Remove a book from the library catalog.")
def delete_book(
    book_id: Annotated[str, Field(description="The book ID to delete")],
) -> dict:
    print(f"[red]invoking tool:delete_book book_id={book_id}[/red]")
    return {
        "status": "deleted",
        "book_id": book_id,
        "deleted_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(name="update_book", description="Update book information in the catalog.")
def update_book(
    book_id: Annotated[str, Field(description="The book ID to update")],
    title: Annotated[str | None, Field(description="New title")] = None,
    author: Annotated[str | None, Field(description="New author")] = None,
    available: Annotated[bool | None, Field(description="Availability status")] = None,
) -> dict:
    print(f"[yellow]invoking tool:update_book book_id={book_id}[/yellow]")
    return {
        "status": "updated",
        "book_id": book_id,
        "title": title or "The Great Gatsby",
        "author": author or "F. Scott Fitzgerald",
        "available": available if available is not None else True,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(name="search_books", description="Search for books by title or author.")
def search_books(
    query: Annotated[str, Field(description="Search query for title or author")],
) -> dict:
    print(f"[blue]invoking tool:search_books query={query}[/blue]")
    return {
        "results": [
            {
                "book_id": "book_001",
                "title": "1984",
                "author": "George Orwell",
                "isbn": "978-0451524935",
                "available": True,
            },
            {
                "book_id": "book_002",
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "isbn": "978-0061120084",
                "available": False,
            },
        ],
        "total": 2,
    }


@mcp.tool(name="get_book_details", description="Get detailed information about a book.")
def get_book_details(
    book_id: Annotated[str, Field(description="The book ID")],
) -> dict:
    print(f"[cyan]invoking tool:get_book_details book_id={book_id}[/cyan]")
    return {
        "book_id": book_id,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "isbn": "978-0316769174",
        "year": 1951,
        "available": True,
        "copies_total": 5,
        "copies_available": 3,
        "location": "Fiction Section, Shelf A3",
    }


@mcp.tool(name="checkout_book", description="Check out a book for a member.")
def checkout_book(
    book_id: Annotated[str, Field(description="The book ID to checkout")],
    member_id: Annotated[str, Field(description="The member ID")],
    due_days: Annotated[int, Field(description="Number of days until due")] = 14,
) -> dict:
    print(
        f"[green]invoking tool:checkout_book book_id={book_id}, member_id={member_id}[/green]"
    )
    return {
        "status": "checked_out",
        "book_id": book_id,
        "member_id": member_id,
        "checkout_date": datetime.now(timezone.utc).isoformat(),
        "due_date": "2026-02-03T10:00:00Z",
        "transaction_id": "txn_98765",
    }


@mcp.tool(name="return_book", description="Return a checked out book to the library.")
def return_book(
    book_id: Annotated[str, Field(description="The book ID to return")],
    member_id: Annotated[str, Field(description="The member ID")],
) -> dict:
    print(
        f"[blue]invoking tool:return_book book_id={book_id}, member_id={member_id}[/blue]"
    )
    return {
        "status": "returned",
        "book_id": book_id,
        "member_id": member_id,
        "return_date": datetime.now(timezone.utc).isoformat(),
        "late_fee": 0.00,
    }


@mcp.tool(name="add_member", description="Register a new library member.")
def add_member(
    name: Annotated[str, Field(description="Member's full name")],
    email: Annotated[str, Field(description="Member's email address")],
    membership_type: Annotated[
        str, Field(description="Type of membership (student, adult, senior)")
    ] = "adult",
) -> dict:
    print(f"[green]invoking tool:add_member name={name}, email={email}[/green]")
    return {
        "status": "registered",
        "member_id": "mem_54321",
        "name": name,
        "email": email,
        "membership_type": membership_type,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "expiry_date": "2027-01-20T00:00:00Z",
    }


@mcp.tool(name="get_member_info", description="Get member information and history.")
def get_member_info(
    member_id: Annotated[str, Field(description="The member ID")],
) -> dict:
    print(f"[cyan]invoking tool:get_member_info member_id={member_id}[/cyan]")
    return {
        "member_id": member_id,
        "name": "Alex Johnson",
        "email": "alex.johnson@example.com",
        "membership_type": "adult",
        "books_checked_out": 2,
        "books_overdue": 0,
        "total_borrowed": 47,
        "member_since": "2020-03-15T00:00:00Z",
    }


@mcp.tool(
    name="get_overdue_books",
    description="Get a list of all overdue books in the system.",
)
def get_overdue_books() -> dict:
    print("[red]invoking tool:get_overdue_books[/red]")
    return {
        "overdue_count": 3,
        "books": [
            {
                "book_id": "book_003",
                "title": "Pride and Prejudice",
                "member_id": "mem_111",
                "member_name": "Sarah Smith",
                "due_date": "2026-01-10T00:00:00Z",
                "days_overdue": 10,
                "late_fee": 5.00,
            },
            {
                "book_id": "book_007",
                "title": "Moby Dick",
                "member_id": "mem_222",
                "member_name": "John Doe",
                "due_date": "2026-01-15T00:00:00Z",
                "days_overdue": 5,
                "late_fee": 2.50,
            },
            {
                "book_id": "book_015",
                "title": "The Hobbit",
                "member_id": "mem_333",
                "member_name": "Emily Brown",
                "due_date": "2026-01-18T00:00:00Z",
                "days_overdue": 2,
                "late_fee": 1.00,
            },
        ],
    }


@mcp.tool(
    name="get_book_info",
    description="Get detailed information about a book given its title.",
)
def get_book_info(
    title: Annotated[str, Field(description="Title of the book")],
) -> dict:
    print(f"[magenta]invoking tool:get_book_info title={title}[/magenta]")

    # Lists for random generation
    authors = [
        "Jane Austen",
        "Mark Twain",
        "Virginia Woolf",
        "Ernest Hemingway",
        "Toni Morrison",
        "Gabriel García Márquez",
        "Haruki Murakami",
        "Margaret Atwood",
        "Chinua Achebe",
        "Isabel Allende",
    ]

    genres = [
        "Fiction",
        "Mystery",
        "Science Fiction",
        "Fantasy",
        "Historical Fiction",
        "Romance",
        "Thriller",
        "Literary Fiction",
        "Dystopian",
        "Adventure",
    ]

    publishers = [
        "Penguin Random House",
        "HarperCollins",
        "Simon & Schuster",
        "Hachette Book Group",
        "Macmillan Publishers",
        "Vintage Books",
        "Knopf",
        "Scribner",
        "Farrar, Straus and Giroux",
        "Grove Press",
    ]

    plot_templates = [
        "A gripping tale of {theme} that explores the depths of human nature.",
        "An epic journey through {theme} that will captivate readers from start to finish.",
        "A thought-provoking exploration of {theme} in modern society.",
        "A riveting story that weaves together themes of {theme} and redemption.",
        "An unforgettable narrative about {theme} and the human condition.",
    ]

    themes = [
        "love and loss",
        "identity and belonging",
        "power and corruption",
        "survival and resilience",
        "family and legacy",
        "truth and deception",
        "freedom and oppression",
        "hope and despair",
        "justice and revenge",
    ]

    # Generate random data
    author = random.choice(authors)
    genre = random.choice(genres)
    publisher = random.choice(publishers)
    year = random.randint(1950, 2025)
    pages = random.randint(150, 800)
    rating = round(random.uniform(3.5, 5.0), 1)
    reviews_count = random.randint(100, 50000)
    isbn = f"978-{random.randint(0, 9)}-{random.randint(100, 999)}-{random.randint(10000, 99999)}-{random.randint(0, 9)}"
    theme = random.choice(themes)
    summary = random.choice(plot_templates).format(theme=theme)

    return {
        "title": title,
        "author": author,
        "genre": genre,
        "publisher": publisher,
        "publication_year": year,
        "pages": pages,
        "isbn": isbn,
        "rating": rating,
        "reviews_count": reviews_count,
        "summary": summary,
        "language": "English",
        "format": random.choice(["Hardcover", "Paperback", "eBook", "Audiobook"]),
        "price": round(random.uniform(9.99, 34.99), 2),
    }


if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "9000"))
    mcp.run(transport="http", host=host, port=port)
