# Name : Malarchelvi S Ganandran
# Student ID : S4109025

"""
Book rental system based on the requirements
This program is built for a book rental service where a receptionist can register customers,
record book rentals, apply membership discounts, and manage rental records. It also lets the
receptionist view and update book categories, track the most valuable customer, and display
a customer's rental history.

Design choices made:
- Used dictionaries to store book categories and the catalog for quick lookups.
- Customers and members are kept in lists since they’re just names and easy to manage that way.
- Used while-loops for input validation so the program only accepts correct inputs and avoids crashing.
- Book names & customer names are matched in lowercase so it's easier to find a book regardless of how the name is typed.

Challenges handled:
- Made sure invalid inputs (like names, book titles, and number of days) are handled smoothly with clear messages.
- Prevented duplicate entries when adding new customers or members.
- Structured the interaction by adding prompts so that the receptionist can move through options easily.

Assumptions made:
- The receptionist is expected to always enter values in the right format (e.g., commas separating book updates).
- Book names are treated as case-insensitive for renting.
- All books entered when updating are assumed to be new (if adding) or already exist (if removing).
- The only membership available is a basic one with 10% discount.
- Price is based on number of days and category rates.
- When updating book info or prices, correct input format is always used.
"""


# --- Initialization ---
book_category_info = {
    "Fantasy": ("Rental", 0.5, 0.4),
    "Crime": ("Rental", 0.5, 0.4),
    "Classics": ("Rental", 0.3, 0.25),
    "Modern Classics": ("Rental", 0.4, 0.3),
    "History": ("Rental", 0.4, 0.3),
    "Philosophy": ("Rental", 0.3, 0.25),
    "Science": ("Rental", 0.5, 0.4),
    "Textbooks": ("Reference", 0.75, 0.6),
    "Art": ("Rental", 0.5, 0.4),
    "Other": ("Reference", 0.5, 0.4)
}

book_catalog = {
    "Fantasy": {
        "Harry Potter 1": (0.5, 0.4),
        "The Hobbit": (0.5, 0.4)
    },
    "Crime": {
        "Gone Girl": (0.5, 0.4),
        "Sherlock Holmes 1": (0.5, 0.4)
    },
    "Classics": {
        "Pride and Prejudice": (0.3, 0.25)
    },
    "Modern Classics": {
        "To Kill a Mockingbird": (0.4, 0.3)
    },
    "History": {
        "The Diary of a Young Girl": (0.4, 0.3)
    },
    "Philosophy": {
        "The Republic": (0.3, 0.25)
    },
    "Science": {
        "A Brief History of Time": (0.5, 0.4)
    },
    "Textbooks": {
        "Introduction to the Theory of Computation": (0.75, 0.6)
    },
    "Art": {
        "The Story of Art": (0.5, 0.4)
    },
    "Other": {
        "Thinking Fast and Slow": (0.5, 0.4),
        "Atomic Habits": (0.5, 0.4)
    }
}

customers = ["Emily", "James"]
members = ["Emily"]

# Track spending and history
customer_spending = {}
rental_logs = {}

# Menu
while True:
    print("\nWelcome to the RMIT book rental service!")
    print("#" * 50)
    print("You can choose from the following options:")
    print("1: Rent a book")
    print("2: Update information of a book category")
    print("3: Update books of a book category")
    print("4: Display existing customers")
    print("5: Display existing book categories")
    print("6: Display the most valuable customer")
    print("7: Display a customer rental history")
    print("0: Exit the program")
    print("#" * 50)
    choice = input("Choose one option: ").strip()

    if choice == "1":
        while True:
            name_input = input("Enter customer's name: ").strip()
            # Allow multiple names with spaces (e.g., "Teddy Bear")
            if all(part.isalpha() for part in name_input.split()):
                break
            print("Error: Name must contain only alphabet characters and spaces.")

        # Capitalize each part of the name (e.g., "teddy bear" -> "Teddy Bear")
        name = ' '.join([part.capitalize() for part in name_input.split()])
        if name not in customers:
            print("Welcome, new customer!")  # Being welcoming
            customers.append(name)

#For ease of reference
        print("Available Books:")
        for category, books in book_catalog.items():
            print(f"{category}:")
            for book in books:
                print(f"  - {book}")

        rented_books = []
        while True:
            while True:
                book_input = input("Enter the book to rent: ").strip().lower()
                found = False
                for category, books in book_catalog.items():
                    for book in books:
                        if book.lower() == book_input:
                            book_category = category
                            book_title = book
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
                else:
                    print("Error: The book entered does not exist in our catalog.")

            book_type = book_category_info[book_category][0]
            while True:
                try:
                    days_input = input("Enter number of borrowing days (or type 'exit' to cancel): ").strip()
                    if days_input.lower() == 'exit':
                        print("Cancelling current book rental...")
                        break  # Exit the rental input
                    days = int(days_input)
                    if days <= 0:
                        raise ValueError
                    if book_type == "Reference" and days > 14:
                        print("This book is a Reference type and cannot be borrowed for more than 14 days.")
                    else:
                        break
                except ValueError:
                    print("Error: Please enter a valid positive whole number.")

            price_per_day = book_catalog[book_category][book_title][0] if days <= 10 else book_catalog[book_category][book_title][1]
            rented_books.append((book_title, days, price_per_day))

            while True:
                more = input("Do you want to rent another book? (y/n): ").strip().lower()
                if more in ["y", "n"]:
                    break
                print("Invalid input. Please enter 'y' or 'n'.")
            if more == "n":
                break

        original_cost = sum(days * price for _, days, price in rented_books)
        discount = original_cost * 0.10 if name in members else 0
        final_cost = original_cost - discount

        customer_spending[name] = customer_spending.get(name, 0) + final_cost
        rental_logs.setdefault(name, []).append({
            "books": rented_books,
            "original_cost": original_cost,
            "discount": discount,
            "final_cost": final_cost
        })

        print("-" * 90)
        print(f"Receipt for {name}")
        print("-" * 90)
        print("Books rented:")
        for title, days, price in rented_books:
            print(f"- {title} for {days} days ({price:.2f} AUD/day)")
        print("-" * 90)
        print(f"Original cost: {original_cost:.2f} (AUD)")
        print(f"Discount: {discount:.2f} (AUD)")
        print(f"Total cost: {final_cost:.2f} (AUD)")

        if name in members:
            print(f"{name} is already a member.")
        else:
            print(f"{name} is currently not a member.")
            become_member = input("Would the customer like to become a member? (yes/no): ").strip().lower()
            while become_member not in ["yes", "no"]:
                become_member = input("Please enter 'yes' or 'no': ").strip().lower()
            if become_member == "yes":
                members.append(name)
                print(f"{name} is now a member!")
            else:
                print(f"{name} chooses not to be a member.")
            print("Thank you!")

        print("\nCurrent customers (non-members):")
        for i, customer in enumerate([c for c in customers if c not in members], 1):
            print(f"  {i}. {customer}")
        print("Current members:")
        for i, member in enumerate(members, 1):
            print(f"  {i}. {member}")

    elif choice == "2":
        while True:
            print("\nCurrent book categories:") #For ease of reference
            for cat, info in book_category_info.items():
                print(f"{cat}: Type={info[0]}, Price1={info[1]}, Price2={info[2]}")
            update_input = input("Enter category, type, price1, price2 (e.g. Fantasy, Rental, 0.4, 0.3): ")
            try:
                parts = [x.strip() for x in update_input.split(",")]
                if len(parts) != 4:
                    raise ValueError("Please enter all 4 fields.")
                category, cat_type, price1, price2 = parts[0], parts[1], float(parts[2]), float(parts[3])
                if cat_type not in ["Rental", "Reference"]:
                    raise ValueError("Invalid type.")
                matched = next((c for c in book_category_info if c.lower() == category.lower()), None)
                if not matched:
                    raise ValueError("Book category not found.")
                book_category_info[matched] = (cat_type, price1, price2)
                print(f"Updated category '{matched}': Type={cat_type}, Price1={price1}, Price2={price2}")
                break
            except ValueError as e:
                print(f"Error: {e}")

    elif choice == "3":
        while True:
            action = input("Do you want to add (a) or remove (r) books? ").strip().lower()
            if action in ["a", "r"]:
                break
            print("Invalid input. Enter 'a' or 'r'.")

        print("\nFull category listing before update:")# For ease of reference
        for category, books in book_catalog.items():
            print(f"{category}:")
            for book in books:
                print(f"  - {book}")

        while True:
            update_input = input("Enter category and book(s) (e.g. Fantasy, Book1, Book2): ")
            parts = [x.strip() for x in update_input.split(",")]
            if len(parts) < 2:
                print("Please enter a category and at least one book.")
                continue
            category_input = parts[0]
            books_to_modify = parts[1:]
            matched_category = next((c for c in book_catalog if c.lower() == category_input.lower()), None)
            if not matched_category:
                print("Book category not found.")
                continue
            if action == 'a':
                existing_books = []
                added_books = []
                for book in books_to_modify:
                    if book in book_catalog[matched_category]:
                        existing_books.append(book)
                    else:
                        price1, price2 = book_category_info[matched_category][1], book_category_info[matched_category][2]
                        book_catalog[matched_category][book] = (price1, price2)
                        added_books.append(book)
                if existing_books:
                    print(f"These books already exist: {existing_books}")
                if added_books:
                    print(f"Books added: {added_books}")
            elif action == 'r':
                not_found = []
                removed = []
                for book in books_to_modify:
                    if book in book_catalog[matched_category]:
                        del book_catalog[matched_category][book]
                        removed.append(book)
                    else:
                        not_found.append(book)
                if removed:
                    print(f"Books removed: {removed}")
                if not_found:
                    print(f"Books not found and not removed: {not_found}")
            break

    elif choice == "4":
        print("\nList of Existing Customers and Memberships:")
        for name in customers:
            membership = "Member" if name in members else "Non-member"
            print(f"- {name}: {membership}")

    elif choice == "5":
        print("\nList of Book Categories and Books:")
        for category, info in book_category_info.items():
            print(f"\n{category}:")
            print(f"  Type: {info[0]}")
            print(f"  Price1: {info[1]} AUD/day")
            print(f"  Price2: {info[2]} AUD/day")
            print("  Books:")
            for book in book_catalog.get(category, []):
                print(f"    - {book}")

    elif choice == "6":
        if not customer_spending:
            print("No rental data available.")
        else:
            max_amount = max(customer_spending.values())
            top_customers = [c for c, amt in customer_spending.items() if amt == max_amount]
            print("Most Valuable Customer(s):")
            for c in top_customers:
                print(f"- {c}: {max_amount:.2f} AUD spent")



    elif choice == "7":

        while True:

            name_input = input("Enter customer name: ").strip()

            name = name_input.title()

            if name not in customers:

                print("Customer not found. Please try again.")

            elif name in customers and name not in rental_logs:

                print(f"{name} has not borrowed any books yet.")

                break

            else:

                print(f"\nThis is the rental history of {name}.")

                print(f"{'':8}Books & Borrowing days{'':20}Original Cost    Discount    Final Cost")

                for i, entry in enumerate(rental_logs[name], 1):
                    book_line = ', '.join([f"{t}: {d} days" for t, d, _ in entry["books"]])

                    print(
                        f"Rental {i:<2}  {book_line:<45} {entry['original_cost']:>6.2f}         {entry['discount']:>5.2f}       {entry['final_cost']:>6.2f}")

                break


    elif choice == "0":
        print("Exiting program. Goodbye!")
        break

    else:
        print("Invalid option.")
