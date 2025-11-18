import logging
import sys
from library_manager.inventory import LibraryInventory
from library_manager.book import Book

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("library-cli")

def prompt(msg: str) -> str:
    return input(msg).strip()

def add_book_flow(inv: LibraryInventory):
    print("\nAdd a new book")
    title = prompt("Title: ")
    author = prompt("Author: ")
    isbn = prompt("ISBN: ")
    if not (title and author and isbn):
        print("All fields are required.")
        return
    inv.add_book(Book(title=title, author=author, isbn=isbn))
    print("Book added successfully.")

def issue_book_flow(inv: LibraryInventory):
    print("\nIssue a book")
    isbn = prompt("ISBN: ")
    if inv.issue_book(isbn):
        print("Book issued.")
    else:
        print("Failed to issue book. Check logs or ISBN/state.")

def return_book_flow(inv: LibraryInventory):
    print("\nReturn a book")
    isbn = prompt("ISBN: ")
    if inv.return_book(isbn):
        print("Book returned.")
    else:
        print("Failed to return book. Check logs or ISBN/state.")

def view_all_flow(inv: LibraryInventory):
    print("\nAll books in catalog:")
    for s in inv.display_all():
        print(" -", s)

def search_flow(inv: LibraryInventory):
    print("\nSearch")
    mode = prompt("Search by (1) Title (2) ISBN: ")
    if mode == "1":
        q = prompt("Enter title substring: ")
        results = inv.search_by_title(q)
        if results:
            for b in results:
                print(" -", b)
        else:
            print("No matches.")
    elif mode == "2":
        q = prompt("Enter ISBN: ")
        b = inv.search_by_isbn(q)
        if b:
            print("Found:", b)
        else:
            print("No book with that ISBN.")
    else:
        print("Invalid choice.")

def main():
    inv = LibraryInventory(json_path="catalog.json")
    while True:
        print("""\nLibrary Inventory Manager
1. Add Book
2. Issue Book
3. Return Book
4. View All
5. Search
6. Exit
""")
        choice = prompt("Choose an option: ")
        try:
            if choice == "1":
                add_book_flow(inv)
            elif choice == "2":
                issue_book_flow(inv)
            elif choice == "3":
                return_book_flow(inv)
            elif choice == "4":
                view_all_flow(inv)
            elif choice == "5":
                search_flow(inv)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            sys.exit(0)
        except Exception as e:
            logger.exception("An unexpected error occurred: %s", e)

if __name__ == '__main__':
    main()
