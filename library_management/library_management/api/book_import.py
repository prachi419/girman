import frappe
import requests
from frappe.model.naming import make_autoname

@frappe.whitelist()
def import_books_from_api(title_filter=None, total_books=20):
    try:
        total_books = int(total_books)
    except Exception:
        frappe.throw("Please enter a valid number for total_books.")

    if total_books <= 0:
        frappe.throw("Please enter a number greater than 0.")

    url = "https://frappe.io/api/method/frappe-library"
    books_inserted = 0
    page = 1

    while books_inserted < total_books:
        params = {
            "page": page
        }
        if title_filter:
            params["title"] = title_filter

        response = requests.get(url, params=params)
        if response.status_code != 200:
            frappe.throw("Failed to fetch data from external API.")

        data = response.json().get("message", [])
        if not data:
            break  # No more results

        for book in data:
            if books_inserted >= total_books:
                break

            book_name = book.get("title")
            isbn = book.get("isbn")

            # Avoid duplicates based on ISBN or book name
            if isbn and frappe.db.exists("Book", {"isbn": isbn}):
                continue

            if frappe.db.exists("Book", {"book_name": book_name}):
                continue

            # Create new Book
            doc = frappe.new_doc("Book")
            doc.book_name = book_name[:140]  # Limit title to 140 chars
            doc.author = book.get("authors")
            doc.isbn = isbn
            doc.total_stock = 10
            doc.available_qty = 5

            # Force unique name in case 'book_name' is title field
            doc.name = make_autoname("BOOK-.#####")

            doc.insert(ignore_permissions=True)
            books_inserted += 1

        page += 1

    return f"{books_inserted} books imported successfully."
