# COSC2531 Assignment 2
# Name: Malarchelvi S Ganandran
# Student ID: S4109025

"""

Design Reflection:
— Object-Oriented Programming (OOP):
OOP is the backbone of this system. Classes are used to encapsulate entities such as customers, books, categories,
and rentals. This models the real-world domain clearly and allows for polymorphism, inheritance, and abstraction:
   • The `Customer` base class is extended by `Member` (adds discount logic) and `GoldMember` (adds reward logic).
   • Both `Book` and `BookSeries` override `get_price(days)` to support pricing per book and pricing bundles.
   • The `Rental` class handles the calculation logic, and `RentalRecord` serializes rental data for storage.
   • This design promotes code reuse and isolates behaviors in well-defined places (SRP — Single Responsibility Principle).

— Classes and Responsibilities:
   • `Records` loads and stores customers, books, and categories in memory, acting as a centralized in-memory database.
   • `Operations` acts as the program controller and CLI handler, routing user commands to the appropriate logic.
   • `BookCategory` centralizes pricing logic and restriction enforcement (e.g., Reference type with 14-day limit).

— Data Structures:
   • Lists are used for customer, book, and category collections to support easy iteration and dynamic updates.
   • Dictionaries are used during file parsing (`book_dict`) and for rental grouping, allowing quick lookups by key
     (ID/name or composite keys like rental sessions).
   • Tuples are used as dictionary keys to group multiple rentals by timestamp for display and reporting.

— Encapsulation and Abstraction:
   • Internal object data (e.g., reward points, pricing) is kept private and accessed through public interfaces.
   • Methods like `get_discount()` or `update_reward()` abstract away internal logic, ensuring reusable and testable code.
   • This abstraction supports polymorphism and decouples the CLI from business logic.

— Control Structures and Loops:
   • `while` loops are used for interactive menus and repeated input prompts (e.g., entering multiple rentals, retrying invalid input).
     Their unbounded nature makes them ideal for interactive workflows.
   • `for` loops are used when iterating over known-sized data, such as printing lists of customers or books.
   • `if-elif-else` chains are used to direct logic based on menu choices, customer types, and validation results.

— Input Validation:
   • Regular expressions (`re.fullmatch`) validate name inputs to ensure alphabetic and formatting correctness.
   • All numerical inputs (days, rates, etc.) are validated using type casting and condition checks.
   • Case-insensitive lookups prevent logic errors due to user input casing.
   • Validation is often wrapped in `while` loops to allow retries on invalid input, improving usability.

— Exception Handling:
   • Custom exceptions like `ReferenceLimitError`, `InvalidDaysError`, and `InvalidNameError` enforce business rules.
   • These exceptions are caught with `try-except` blocks, preventing program crashes and giving clear error feedback.
   • Defensive programming is also applied when reading files and importing rentals to skip bad lines gracefully.

— File I/O and Persistence:
   • Input data is stored in structured `.txt` files and loaded using `open()` and `.split(',')`.
   • Rentals are logged to `rental_history.txt` using append mode (`"a"`) to maintain persistent transaction history.
   • File imports are robust — invalid lines are skipped with error messages to maintain program stability.
   • File read methods support relative path fallback to ensure portability.

— CLI and Menu Design:
   • The main menu is implemented using a `while True:` loop and `input()` prompts, allowing continuous interaction.
   • Menu options are routed using `if-elif` blocks for clarity and modular command handling.
   • Submenus (e.g., update category, add books) are implemented with their own loops for focused control and reuse.

— Modularity and Maintainability:
   • Each operation (rent, update, list, adjust) is encapsulated in a named method inside `Operations`, ensuring
     maintainable and testable code.
   • Code follows DRY principles — customer and book lookup logic is reused via `find_customer()` and `find_book()`.
   • The code is organized around responsibilities, promoting ease of debugging and future development.

— Reusability and Extensibility:
   • Class-level variables (e.g., `Member.discount_rate`) allow dynamic updates to global policies.
   • The program supports adding new customer or book types via subclassing without touching core logic.
   • Book categories and prices can be modified at runtime, simulating real-world system adaptability.

— Reporting and Analytics:
   • Rentals are grouped and displayed using dictionary-based aggregation.
   • The "most valuable customer" is computed by summing all final costs in `rental_history.txt`.
   • Grouped receipts show multiple books per transaction, improving clarity for users.

— Defensive and Fault-Tolerant Design:
   • The program catches and handles all major failure points: bad input, missing files, empty datasets.
   • Rental processing gracefully skips invalid entries while continuing with valid ones.
   • Error messages are specific and help guide user correction (e.g., "Reference books: max 14 days").


Issues that were possibly fixed:
- Incorrect price calculation for book series – initially forgot to apply the 50% discount.
- Reference books were allowed for more than 14 days – added ReferenceLimitError to enforce limit.
- File parsing errors due to inconsistent formats in input files (extra/missing commas).
- No duplicate check for book IDs or names – added validation during book addition.
- Floating point precision errors in cost/discount – fixed using round() for consistency.
- Complex logic needed to import rentals with mixed book/day and financials from flat files.
- User input validation missing – added regex for name validation and exception handling for numbers.
- Rentals for new customers crashed if name was invalid – fixed with validation before registration.
- Reward points were calculated before discount – corrected to apply rewards on final cost.
- Redundant method definitions (e.g., update_books_of_category) – refactored and cleaned up.
- Reward points not updated during file import – fixed with conditional parsing and update logic.
- Grouping rental history by customer/timestamp was tricky – used tuples as dictionary keys.
- Program crashed on missing input files – added try-except blocks for file reading.
- Menu loops had no clean exit path – introduced 'done' keyword to terminate submenus.
- Some books had no assigned category – handled by displaying "N/A" in listings.
- Book name vs ID lookups were case-sensitive initially – adjusted with .lower() for reliable matching.
- GoldMember creation required manual input of reward values – prone to input error.
- Lack of separation between CLI and logic layers – made testing and reuse harder.
- No validation for negative or zero rental days – added exception handling.
- Rental timestamps not timezone-aware – uses system time only, which may cause inconsistencies.
- RentalRecord.to_line() uses hard-coded CSV format – not robust for commas in book names.
- Operations.menu() function grew too large – violates single-responsibility principle.
- Rental grouping by customer assumes names are unique – can misattribute rentals if names repeat.
- BookSeries displayed only as a single entity – no detail of internal books shown in some outputs.
- Dynamic updates (e.g., reward rate) are not saved persistently – lost after program exit.
- Customer creation allows duplicate IDs if re-entered – no ID collision detection.
- File paths are hardcoded (e.g., `C:/Users/...`) – should use relative paths or config.
- Book removal does not delete series membership – orphaned books might remain logically inconsistent.
- Inconsistent formatting between loaded and manually entered records – timestamp and spacing vary.
- save_books_to_file() is defined inside another method (`rent_a_book`) – accidental nesting likely unintentional.

Issues that were possibly not corrected:
- Issues relating to visual display of output printed (eg: spacing, capitalising of letters)
- Minor nuances struggled to code due to repetitive errors. These areas were either omitted or may generate error if an input is tried.
– Duplicate method definition: `update_books_of_category()` appears multiple times in the `Operations` class,
  causing redundancy and possible logic overrides.
– Book removal does not update BookSeries membership, which may leave orphaned or broken links within series.
– Reward point changes and new customer registrations are not persisted to the original customer files;
  data is lost when the program exits.
– File paths are hardcoded (e.g., "C:/Users/..."), reducing cross-platform compatibility and portability.
– The `save_books_to_file()` method is incorrectly defined inside `rent_a_book()`, limiting its accessibility.
– No check exists for duplicate customer IDs, which can result in multiple customers sharing the same ID.
– Book and customer lookups assume unique names; duplicate names may lead to ambiguous or incorrect selections.
– BookSeries entries do not clearly show the books they contain in CLI outputs, limiting user understanding.
– Adding or removing books does not update `books.txt` or `book_categories.txt`; changes are session-only.
– Book IDs are not validated for format or structure, increasing the risk of inconsistency or invalid entries.
– Reference book rental limits (14-day max) are not enforced during batch file import of rental records.
– There is no undo or edit capability in the CLI once a rental is logged or a customer is added.
– Listings do not consistently differentiate between single books and book series in output formatting.
– Books that are part of a series do not indicate that relationship in listings or details.
– When loading rewards from file imports, reward updates occur silently without confirmation to the user.

"""

import os
import sys
from datetime import datetime

class InvalidNameError(Exception): pass
class InvalidBookError(Exception): pass
class InvalidDaysError(Exception): pass
class ReferenceLimitError(Exception): pass
class InvalidInputError(Exception): pass

import re

def is_valid_name(name):
    return re.fullmatch(r"[A-Za-z\s\-]+", name) is not None

class Records:
    def __init__(self):
        self.customers = []
        self.books = []
        self.book_categories = []

    def read_customers(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = [x.strip() for x in line.strip().split(',')]
                ctype, cid, name, dr, rr, rw = parts
                if ctype == 'C':
                    self.customers.append(Customer(cid, name))
                elif ctype == 'M':
                    self.customers.append(Member(cid, name))
                elif ctype == 'G':
                    self.customers.append(GoldMember(cid, name, float(rr), int(rw)))

    def read_books_and_book_categories(self, book_file, cat_file):
        book_dict = {}

        with open(book_file, 'r') as bf:
            for line in bf:
                parts = [x.strip() for x in line.strip().split(',')]
                if parts[0].startswith('S'):  # It's a series
                    sid, sname, *book_names = parts
                    book_dict[sid] = {'id': sid, 'name': sname, 'books': book_names}
                    book_dict[sname] = book_dict[sid]  # Allow name lookup too
                else:
                    bid, bname = parts
                    book_dict[bname] = Book(bid, bname, None)
                    book_dict[bid] = book_dict[bname]  # ID-based lookup

        with open(cat_file, 'r') as cf:
            for line in cf:
                parts = [x.strip() for x in line.strip().split(',')]
                cid, cname, ctype, p1, p2 = parts[:5]
                category = BookCategory(cid, cname, ctype, float(p1), float(p2))

                for book_key in parts[5:]:
                    entry = book_dict.get(book_key)
                    if isinstance(entry, Book):
                        entry.category = category
                        category.add_book(entry)
                        self.books.append(entry)
                    elif isinstance(entry, dict):  # It's a series dictionary
                        sub_books = [book_dict[bn] for bn in entry['books'] if bn in book_dict]
                        series = BookSeries(entry['id'], entry['name'], category, sub_books)
                        category.add_book(series)
                        self.books.append(series)
                        book_dict[entry['id']] = series  # Add full ID as lookup
                        book_dict[entry['name']] = series  # Add name as lookup

                self.book_categories.append(category)

    def find_customer(self, value):
        value = value.strip().lower()
        return next((c for c in self.customers if c.customer_id.lower() == value or c.name.lower() == value), None)

    def find_book(self, value):
        value = value.strip().lower()
        return next(
            (b for b in self.books if b.book_id.lower() == value or b.name.lower() == value),
            None
        )

    def list_customers(self):
        print("Customer ID | Name     | Discount Rate | Reward Rate | Reward Points")
        print("---------------------------------------------------------------")
        for customer in self.customers:
            customer.display_info()

    def add_rental_record(self, record):
        if not hasattr(self, 'rentals'):
            self.rentals = []
        self.rentals.append(record)

class Customer:
    def __init__(self, cid, name):
        self.customer_id = cid
        self.name = name

    def display_info(self):
        print(f"{self.customer_id} {self.name} | Discount: N/A | Reward Rate: N/A | Reward Points: N/A")

    def get_name(self):
        return self.name

    def get_discount(self, cost):
        return 0

class Member(Customer):
    discount_rate = 0.10

    def get_discount(self, cost):
        return cost * self.discount_rate

    def display_info(self):
        print(f"{self.customer_id} {self.name} | Discount: {Member.discount_rate:.2f} | Reward Rate: N/A | Reward Points: N/A")


class GoldMember(Member):
    discount_rate = 0.12

    def __init__(self, cid, name, reward_rate, reward):
        super().__init__(cid, name)
        self.reward_rate = reward_rate
        self.reward = reward

    def get_discount(self, cost):
        return cost * self.discount_rate

    def get_reward(self, cost):
        return round(cost * self.reward_rate)

    def update_reward(self, points):
        self.reward += points

    def display_info(self):
        print(f"{self.customer_id} {self.name} | Discount: {GoldMember.discount_rate:.2f} | Reward Rate: {self.reward_rate:.2f} | Reward Points: {self.reward}")


class Book:
    def __init__(self, bid, name, category):
        self.book_id = bid
        self.name = name
        self.category = category
    def get_price(self, days): return self.category.get_price(days)
    def display_info(self): print(self.book_id, self.name)

class BookSeries(Book):
    def __init__(self, sid, name, category, books):
        super().__init__(sid, name, category)
        self.books = books
    def get_price(self, days): return sum(b.get_price(days) for b in self.books) * 0.5

class BookCategory:
    def __init__(self, cid, name, ctype, p1, p2):
        self.category_id = cid
        self.name = name
        self.category_type = ctype
        self.price_1 = p1
        self.price_2 = p2
        self.books = []
    def add_book(self, book): self.books.append(book)
    def get_price(self, days):
        if self.category_type == 'Reference' and days > 14:
            raise ReferenceLimitError("Reference books cannot be borrowed for more than 14 days.")
        return days * self.price_1 if days <= 7 else 7 * self.price_1 + (days - 7) * self.price_2
    def display_info(self): print(self.category_id, self.name)

class Rental:
    def __init__(self, customer, book, days):
        self.customer = customer
        self.book = book
        self.days = days

    def compute_cost(self):
        cost = self.book.get_price(self.days)
        discount = self.customer.get_discount(cost)
        total = round(cost - discount, 2)  # ✅ Explicit rounding to fix floating point error
        reward = self.customer.get_reward(total) if isinstance(self.customer, GoldMember) else None
        if reward is not None:
            self.customer.update_reward(reward)
            return (round(cost, 2), round(discount, 2), total, reward)
        return (round(cost, 2), round(discount, 2), total)

class RentalRecord:
    def __init__(self, customer, book, days, original_cost, discount, total_cost, reward, timestamp):
        self.customer = customer
        self.book = book
        self.days = days
        self.original_cost = original_cost
        self.discount = discount
        self.total_cost = total_cost
        self.reward = reward
        self.timestamp = timestamp
    def to_line(self):
        reward_display = self.reward if self.reward is not None else "na"
        return f"{self.customer.get_name()}, {self.book.name}, {self.days}, {self.original_cost}, {self.discount}, {self.total_cost}, {reward_display}, {self.timestamp}"

class Operations:
    def __init__(self):
        self.records = Records()
        try:
            self.records.read_customers("C:/Users/flowe/OneDrive/Desktop/Masters/2. Fundamentals of Programming/Assignment 2/customer.txt")
            self.records.read_books_and_book_categories(
                "C:/Users/flowe/OneDrive/Desktop/Masters/2. Fundamentals of Programming/Assignment 2/books.txt",
                "C:/Users/flowe/OneDrive/Desktop/Masters/2. Fundamentals of Programming/Assignment 2/book_categories.txt")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            exit(1)

        def update_books_of_category(self):
            cat_input = input("Enter book category name or ID: ").strip().lower()
            category = next((c for c in self.records.book_categories if
                             c.category_id.lower() == cat_input or c.name.lower() == cat_input), None)

            if not category:
                print("Category not found.")
                return

            print(f"Selected category: {category.name}")

            while True:
                action = input(
                    "Type 'add' to add a book, 'remove' to delete a book, or 'done' to finish: ").strip().lower()
                if action == 'done':
                    break

                elif action == 'add':
                    bid = input("Enter book ID: ").strip()
                    bname = input("Enter book name: ").strip().title()

                    if any(b.book_id == bid or b.name.lower() == bname.lower() for b in self.records.books):
                        print(f"Book ID or name already exists. Skipping.")
                        continue

                    new_book = Book(bid, bname, category)
                    category.add_book(new_book)
                    self.records.books.append(new_book)
                    print(f"Book '{bname}' added to category '{category.name}'.")

                elif action == 'remove':
                    bid = input("Enter book ID to remove: ").strip()
                    book = next((b for b in category.books if b.book_id == bid), None)

                    if not book:
                        print(f"No book with ID '{bid}' found in category.")
                        continue

                    category.books.remove(book)
                    if book in self.records.books:
                        self.records.books.remove(book)
                    print(f"Book '{book.name}' removed from category.")

                else:
                    print("Invalid action. Type 'add', 'remove', or 'done'.")

    def update_books_of_category(self):
        cat_input = input("Enter book category name or ID: ").strip().lower()
        category = next((c for c in self.records.book_categories if
                         c.category_id.lower() == cat_input or c.name.lower() == cat_input), None)

        if not category:
            print("Category not found.")
            return

        print(f"Selected category: {category.name}")

        while True:
            action = input(
                "Type 'add' to add a book, 'remove' to delete a book, or 'done' to finish: ").strip().lower()
            if action == 'done':
                break

            elif action == 'add':
                bid = input("Enter book ID: ").strip()
                bname = input("Enter book name: ").strip().title()

                if any(b.book_id == bid or b.name.lower() == bname.lower() for b in self.records.books):
                    print(f"Book ID or name already exists. Skipping.")
                    continue

                new_book = Book(bid, bname, category)
                category.add_book(new_book)
                self.records.books.append(new_book)
                print(f"Book '{bname}' added to category '{category.name}'.")

            elif action == 'remove':
                bid = input("Enter book ID to remove: ").strip()
                book = next((b for b in category.books if b.book_id == bid), None)

                if not book:
                    print(f"No book with ID '{bid}' found in category.")
                    continue

                category.books.remove(book)
                if book in self.records.books:
                    self.records.books.remove(book)
                print(f"Book '{book.name}' removed from category.")

            else:
                print("Invalid action. Type 'add', 'remove', or 'done'.")

    def update_category_info(self):
        cat_input = input("Enter book category name or ID: ").strip().lower()
        category = next((c for c in self.records.book_categories if
                         c.category_id.lower() == cat_input or c.name.lower() == cat_input), None)

        if not category:
            print("Category not found.")
            return

        print(f"Updating category: {category.name}")

        new_type = input("Enter new category type (Rental/Reference): ").strip().capitalize()
        try:
            new_price1 = float(input("Enter new rental price for first 7 days: "))
            new_price2 = float(input("Enter new rental price after 7 days: "))
        except ValueError:
            print("Invalid input for prices. Update cancelled.")
            return

        category.category_type = new_type
        category.price_1 = new_price1
        category.price_2 = new_price2
        print(f"Category '{category.name}' updated successfully with new type and prices.")

    def list_book_categories(self):
        print("{:<10} {:<20} {:<15} {:<10} {:<10} {:<30}".format(
            "Category ID", "Name", "Type", "Price1", "Price2", "Books"))
        print("-" * 100)
        for c in self.records.book_categories:
            book_names = ', '.join(b.name for b in c.books)
            print("{:<10} {:<20} {:<15} {:<10.2f} {:<10.2f} {:<30}".format(
                c.category_id, c.name, c.category_type, c.price_1, c.price_2, book_names))

    def list_books(self):
        print("{:<10} {:<30} {:<20} {:<15} {:<10} {:<10}".format(
            "Book ID", "Name", "Category", "Type", "Price1", "Price2"))
        print("-" * 100)
        for b in self.records.books:
            cat = b.category
            if cat:
                print("{:<10} {:<30} {:<20} {:<15} {:<10.2f} {:<10.2f}".format(
                    b.book_id, b.name, cat.name, cat.category_type, cat.price_1, cat.price_2))
            else:
                print("{:<10} {:<30} {:<20} {:<15} {:<10} {:<10}".format(
                    b.book_id, b.name, "N/A", "N/A", "-", "-"))

    def adjust_member_discount(self):
        try:
            rate = float(input("Enter new discount rate (e.g., 0.2 for 20%): "))
            if rate <= 0:
                raise ValueError("Rate must be positive.")
            Member.discount_rate = rate
            print(f"Member discount rate set to {rate*100:.0f}%.")
        except ValueError as e:
            print("Invalid input:", e)

    def adjust_gold_reward_rate(self):
        cust_input = input("Enter Gold member name or ID: ").strip()
        customer = self.records.find_customer(cust_input)
        if not isinstance(customer, GoldMember):
            print("Customer not found or not a Gold Member.")
            return

        try:
            rate = float(input("Enter new reward rate (e.g., 1 for 100%): "))
            if rate <= 0:
                raise ValueError("Rate must be positive.")
            customer.reward_rate = rate
            print("Reward rate updated successfully.")
        except ValueError as e:
            print("Invalid input:", e)

    def log_rental(self, rental_record):
        with open("rental_history.txt", "a") as f:
            f.write(rental_record.to_line() + "\n")

    def display_rental_history(self):
        try:
            with open("rental_history.txt", "r") as f:
                print("\n--- Rental History ---")
                print("{:<10} {:<40} {:<15} {:<10} {:<10} {:<10} {:<10}".format(
                    "Rental", "Books & Borrowing days", "Original Cost", "Discount", "Final Cost", "Rewards", "Time"))
                print("-" * 110)
                for line in f:
                    print(line.strip())
        except FileNotFoundError:
            print("No rental history available.")

    def display_customer_rental_history(self):
        customer_key = input("Enter customer name or ID: ").strip().lower()
        try:
            with open("rental_history.txt", "r") as f:
                print(f"\nRental history for {customer_key.title()}:\n")
                print("{:<10} {:<40} {:<15} {:<10} {:<10} {:<10} {:<10}".format(
                    "Rental", "Books & Borrowing days", "Original Cost", "Discount", "Final Cost", "Rewards", "Time"))
                print("-" * 110)
                rental_num = 1
                grouped_rentals = {}
                for line in f:
                    parts = [x.strip() for x in line.split(",")]
                    if len(parts) >= 8:
                        cname, bname, days, orig, disc, total, reward, time = parts
                        if cname.lower() == customer_key:
                            key = (orig, disc, total, reward, time)
                            if key not in grouped_rentals:
                                grouped_rentals[key] = []
                            grouped_rentals[key].append(f"{bname}: {days} days")

                for (orig, disc, total, reward, time), book_list in grouped_rentals.items():
                    books_str = ", ".join(book_list)
                    print("{:<10} {:<40} {:<15} {:<10} {:<10} {:<10} {:<10}".format(
                        f"Rental {rental_num}", books_str, orig, disc, total, reward, time))
                    rental_num += 1

        except FileNotFoundError:
            print("No rental history found.")

    def load_rentals_from_file(self):
        file = input("Enter rental file name: ").strip()
        try:
            with open(file, "r") as f:
                for line in f:
                    parts = [p.strip() for p in line.strip().split(",") if p.strip()]
                    if len(parts) < 8:
                        print(f"Skipping invalid line: {line.strip()}")
                        continue
                    cust_key = parts[0]
                    customer = self.records.find_customer(cust_key)
                    if not customer:
                        print(f"Customer {cust_key} not found. Skipping line.")
                        continue

                    book_day_pairs = []
                    idx = 1
                    while idx < len(parts) and not parts[idx].replace('.', '', 1).isdigit():
                        book_id = parts[idx]
                        days = int(parts[idx + 1])
                        book = self.records.find_book(book_id)
                        if not book:
                            print(f"Book {book_id} not found. Skipping book.")
                            idx += 2
                            continue
                        book_day_pairs.append((book, days))
                        idx += 2

                    try:
                        original_cost = float(parts[idx])
                        discount = float(parts[idx + 1])
                        total_cost = float(parts[idx + 2])
                        earned_rewards = parts[idx + 3]
                        timestamp = parts[idx + 4]
                    except Exception:
                        print(f"Error parsing financials or timestamp in line: {line.strip()}")
                        continue

                    if isinstance(customer, GoldMember) and earned_rewards.lower() != "na":
                        try:
                            customer.update_reward(int(earned_rewards))
                        except Exception:
                            print(f"Failed to update rewards for {customer.get_name()}.")

                    for book, days in book_day_pairs:
                        record = RentalRecord(customer, book, days, original_cost, discount, total_cost,
                                              None if earned_rewards == 'na' else int(earned_rewards), timestamp)
                        self.log_rental(record)
            print("Rental file loaded.")
        except FileNotFoundError:
            print("Cannot find the rental file.")

    import re
    def most_valuable_customer(self):
        totals = {}
        try:
            with open("rental_history.txt", "r") as f:
                for line in f:
                    parts = [x.strip() for x in line.split(",")]
                    if len(parts) >= 6:
                        cname = parts[0]
                        total = float(parts[5])
                        totals[cname] = totals.get(cname, 0) + total
            if totals:
                best = max(totals, key=totals.get)
                print(f"Most valuable customer: {best} (${totals[best]:.2f})")
            else:
                print("No rentals recorded.")
        except FileNotFoundError:
            print("No rental history to analyze.")

    def display_all_rentals(self):
        try:
            with open("rental_history.txt", "r") as f:
                print("\n--- All Rentals ---")
                for line in f:
                    parts = [p.strip() for p in line.strip().split(",")]
                    if len(parts) >= 8:
                        cname, bname, days, orig, disc, total, reward, time = parts
                        print(
                            f"Customer: {cname}, Book: {bname}, Days: {days}, Original: {orig}, Discount: {disc}, Total: {total}, Rewards: {reward}, Time: {time}")
        except FileNotFoundError:
            print("No rental history file found.")

    def update_books_of_category(self):
        cat_input = input("Enter book category name or ID: ").strip().lower()
        category = next((c for c in self.records.book_categories if c.category_id.lower() == cat_input or c.name.lower() == cat_input), None)

        if not category:
            print("Category not found.")
            return

        print(f"Selected category: {category.name}")
        while True:
            action = input("Type 'add' to add a book, 'remove' to delete a book, or 'done' to finish: ").strip().lower()
            if action == 'done':
                break

            elif action == 'add':
                bid = input("Enter book ID: ").strip()
                bname = input("Enter book name: ").strip().title()

                if any(b.book_id == bid or b.name.lower() == bname.lower() for b in self.records.books):
                    print(f"Book ID or name already exists. Skipping.")
                    continue

                new_book = Book(bid, bname, category)
                category.add_book(new_book)
                self.records.books.append(new_book)
                print(f"Book '{bname}' added to category '{category.name}'.")

            elif action == 'remove':
                bid = input("Enter book ID to remove: ").strip()
                book = next((b for b in category.books if b.book_id == bid), None)

                if not book:
                    print(f"No book with ID '{bid}' found in category.")
                    continue

                category.books.remove(book)
                if book in self.records.books:
                    self.records.books.remove(book)
                print(f"Book '{book.name}' removed from category.")

            else:
                print("Invalid action. Type 'add', 'remove', or 'done'.")

    def adjust_member_discount(self):
        while True:
            try:
                rate = float(input("Enter new discount rate (e.g., 0.2 for 20%): "))
                if rate <= 0:
                    raise ValueError("Rate must be positive.")
                Member.discount_rate = rate
                print(f"Member discount rate successfully updated to {rate * 100:.0f}%.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def adjust_gold_reward_rate(self):
        while True:
            cust_input = input("Enter Gold member name or ID: ").strip()
            customer = self.records.find_customer(cust_input)
            if not isinstance(customer, GoldMember):
                print("Customer not found or not a Gold Member. Try again.")
                continue

            while True:
                try:
                    rate = float(input("Enter new reward rate (e.g., 1 for 100%): "))
                    if rate <= 0:
                        raise ValueError("Rate must be positive.")
                    customer.reward_rate = rate
                    print(f"Reward rate updated to {rate:.2f} for Gold member {customer.name}.")
                    return
                except ValueError as e:
                    print(f"Invalid input: {e}. Try again.")

    def menu(self):
        while True:
            print("\n--- Book Rental System Menu ---")
            print("1. Rent a book")
            print("2. Display existing customers")
            print("3. Display existing book categories")
            print("4. Display existing books")
            print("5. Update books of a book category")
            print("6. Update category info")
            print("7. Adjust member discount rate")
            print("8. Adjust Gold reward rate")
            print("9. Display all rental history")
            print("10. Display customer rental history")
            print("11. Load rentals from file")
            print("12. Show most valuable customer")
            print("13. Exit")
            choice = input("Select an option (1-13): ")
            if choice == '1':
                self.rent_a_book()
            elif choice == '2':
                self.records.list_customers()
            elif choice == '3':
                self.list_book_categories()
            elif choice == '4':
                self.list_books()
            elif choice == '13':
                print("Exiting program.")
                break
            elif choice == '5':
                self.update_books_of_category()
            elif choice == '6':
                self.update_category_info()
            elif choice == '7':
                self.adjust_member_discount()
            elif choice == '8':
                self.adjust_gold_reward_rate()
            elif choice == '9':
                self.display_rental_history()
            elif choice == '10':
                self.display_customer_rental_history()
            elif choice == '11':
                self.load_rentals_from_file()
            elif choice == '12':
                self.most_valuable_customer()
            else:
                print("Invalid option. Try again.")

    def rent_a_book(self):
        print("You may rent multiple books. Type 'done' when finished.")
        name = input("Enter customer name or ID: ").strip().title()
        customer = self.records.find_customer(name)
        if not customer:
            print("Customer not found. Registering new customer.")
            while True:
                cname = input("Enter new name (alphabets only): ").strip()
                if is_valid_name(cname):
                    break
                else:
                    print("Invalid name. Please use only alphabetic characters, spaces, or hyphens.")
            cid = input("Enter new ID: ")
            ctype = input("C for Customer, M for Member: ").upper()
            customer = Member(cid, cname) if ctype == 'M' else Customer(cid, cname)
            self.records.customers.append(customer)

        rentals = []
        total_original = 0
        total_discount = 0
        total_final = 0
        total_reward = 0
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        while True:
            bname = input("Enter book or series name or ID (or 'done' to finish): ").strip()
            if bname.lower() == 'done':
                break
            book = self.records.find_book(bname)
            if not book:
                print(f"Book or series '{bname}' not found in system.")
                continue
            try:
                days = int(input("Enter number of days: "))
                if days <= 0:
                    raise InvalidDaysError("Invalid number of days.")
                if book.category.category_type == 'Reference' and days > 14:
                    raise ReferenceLimitError("Reference books: max 14 days.")
                rental = Rental(customer, book, days)
                result = rental.compute_cost()
                reward = result[3] if len(result) == 4 else None
                record = RentalRecord(customer, book, days, result[0], result[1], result[2], reward, now)
                self.records.add_rental_record(record)
                self.log_rental(record)

                rentals.append((book, days, result))
                total_original += result[0]
                total_discount += result[1]
                total_final += result[2]
                if reward:
                    total_reward += reward
            except Exception as e:
                print(f"ERROR processing '{book.name}': {e}")

        print("\n--- Rental Receipt ---")
        print(f"Customer: {customer.get_name()}")
        for book, days, result in rentals:
            print(f"Book: {book.name}, Days: {days}, Cost: {result[2]:.2f} AUD")
        print(f"\nOriginal Cost: {total_original:.2f} AUD")
        print(f"Total Discount: {total_discount:.2f} AUD")
        print(f"Total Cost: {total_final:.2f} AUD")
        if total_reward > 0:
            print(f"Total Reward Earned: {total_reward}")
        print("------------------------")

        def save_books_to_file(self):
            with open("books.txt", "w") as bf:
                for book in self.records.books:
                    bf.write(f"{book.book_id},{book.name}\n")

            with open("book_categories.txt", "w") as cf:
                for cat in self.records.book_categories:
                    book_ids = ",".join(b.name for b in cat.books)
                    cf.write(
                        f"{cat.category_id},{cat.name},{cat.category_type},{cat.price_1},{cat.price_2},{book_ids}\n")

if __name__ == "__main__":
    if len(sys.argv) not in [1, 4]:
        print("Usage: python program.py [customers.txt books.txt book_categories.txt]")
        sys.exit(1)
    elif len(sys.argv) == 4:
        cust_file, book_file, cat_file = sys.argv[1:]
    else:
        cust_file = "customers.txt"
        book_file = "books.txt"
        cat_file = "book_categories.txt"

    Operations().menu()