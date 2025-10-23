"""Övning 1:

Skapa en klass bok som ska ha titel, författar, upplaga som attribut.
Titel ska vara en sträng, författare ska vara en sträng och upplaga ska vara en positiv integer!



Skriv ett program som kan lägga till en bok i en lista med böcker!
Programmet ska också kunna skriva ut titel på alla böcker som finns i listan, skriva ut alla författare som finns i listan.
Vi ska också kunna skriva ut all information om böckerna i listan!

Exempel:

Skapa bok
Skriv ut alla titlar
Skriv ut alla författare
Skriv ut alla böcker
Avsluta


ADVANCED:

Gör författare till en klass och ta in ett objekt Författare istället för en sträng på en bok. Sedan också, när vi ska skriva ut alla författare vill vi bara skriva ut alla författare endast en gång!!

"""
class Book:
    def __init__(self, title:str, author:str, edition:int):
        self.title = title
        self.author = author
        self.edition= edition

    def __str__(self):
        return f"Book title: {self.title}, author: {self.author}, edition: {self.edition}"


class Books:
    def __init__(self):
        self.books = []

    @staticmethod
    def validate_title(title):
        if not title:
            print("Title cannot be empty!")
            return False
        return True

    @staticmethod
    def validate_author(author):
        if not author:
            print("Author name cannot be empty!")
            return False
        return True

    @staticmethod
    def validate_edition(edition):
        try:
            edition = int(edition)

            if edition <= 0:
                print("Edition must be greater than 0!")
                return False

        except ValueError:
            print("Edition must be a whole number!")
            return False

        return True

    def validate_new_book(self, new_book_title, new_book_author, new_book_edition):
        for book in self.books:
            if book.title == new_book_title and book.author == new_book_author and book.edition == new_book_edition:
                print(f"We have a registered book with title: {new_book_title}, author: {new_book_author}, edition: {new_book_edition} ")
                return False
        return True

    @staticmethod
    def str_add_book(new_book_title, new_book_author, new_book_edition):
        return f"New book with title: {new_book_title}, author: {new_book_author}, edition: {new_book_edition}"



    def add_book(self):
        while True:
            title = input("Enter book title: ").strip()
            if not self.validate_title(title):
                continue

            author = input("Enter book author: ").strip()
            if not self.validate_author(author):
                continue

            edition = input("Enter book edition: ").strip()
            if not self.validate_edition(edition):
                continue

            if not self.validate_new_book(title, author, edition):
                continue

            edition = int(edition)


            book = Book(title, author, edition)
            self.books.append(book)
            print(f"✅ Added new book: {book}")
            return book

    def get_all_titles(self):
        if not self.books:
            print("No books yet!")
            return
        for book in self.books:
            print(book.title)

    def get_all_authors(self):
        if not self.books:
            print("No books yet!")
            return
        for book in self.books:
            print(book.author)

    def get_books_info(self):
        if not self.books:
            print("No books yet!")
            return
        for book in self.books:
            print(book)






books = Books()
print("Welcome to book manager!")
while True:
    print()
    print("1- Add a book")
    print("2- See all book titles")
    print("3- See all authors")
    print("4- See all books")
    print("0- Exit")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        books.add_book()

    elif choice == "2":
        books.get_all_titles()

    elif choice == "3":
        books.get_all_authors()

    elif choice == "4":
        books.get_books_info()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Not valid choice!")

