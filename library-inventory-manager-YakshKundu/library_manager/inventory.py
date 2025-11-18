import json
import logging
from pathlib import Path
from typing import List, Optional
from .book import Book

logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, json_path: str = "catalog.json"):
        self.json_path = Path(json_path)
        self.books: List[Book] = []
        self.load()

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        logger.info("Added book: %s", book)
        self.save()

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def search_by_title(self, title_substr: str) -> List[Book]:
        q = title_substr.lower()
        return [b for b in self.books if q in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.find_by_isbn(isbn)

    def display_all(self) -> List[str]:
        return [str(b) for b in self.books]

    def issue_book(self, isbn: str) -> bool:
        book = self.find_by_isbn(isbn)
        if not book:
            logger.error("Issue failed. ISBN not found: %s", isbn)
            return False
        if book.issue():
            logger.info("Book issued: %s", book)
            self.save()
            return True
        logger.error("Book already issued: %s", book)
        return False

    def return_book(self, isbn: str) -> bool:
        book = self.find_by_isbn(isbn)
        if not book:
            logger.error("Return failed. ISBN not found: %s", isbn)
            return False
        if book.return_book():
            logger.info("Book returned: %s", book)
            self.save()
            return True
        logger.error("Book already available: %s", book)
        return False

    def save(self) -> None:
        try:
            data = [b.to_dict() for b in self.books]
            self.json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            logger.info("Catalog saved to %s", self.json_path)
        except Exception as e:
            logger.exception("Failed to save catalog: %s", e)

    def load(self) -> None:
        try:
            if not self.json_path.exists():
                logger.info("Catalog file not found, creating new: %s", self.json_path)
                self.save()
                return
            raw = self.json_path.read_text(encoding="utf-8")
            data = json.loads(raw) if raw.strip() else []
            self.books = [Book(**item) for item in data]
            logger.info("Loaded %d books from %s", len(self.books), self.json_path)
        except json.JSONDecodeError:
            logger.error("Catalog file corrupted. Backing up and starting fresh.")
            backup = self.json_path.with_suffix(".corrupt.json")
            self.json_path.replace(backup)
            self.books = []
            self.save()
        except Exception as e:
            logger.exception("Failed to load catalog: %s", e)
