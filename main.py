from Product import Products
from Receipt import Receipt, Receipts


def set_up():
    products = Products()
    products.load_products()

    while True:
        print()
        print("KASSA")
        print("1. Ny kund")
        print("2. Avsluta")
        print()

        choice =input("Choose an option: ")
        print()

        if choice == "1":

            receipts_manager = Receipts()
            receipt_no =receipts_manager.receipt_no

            receipt = Receipt(receipt_no, products=products)
            print(receipt.new_receipt())
            receipts_manager.save_receipt(receipt)
        elif choice == "2":
            break
        else:
            print("Invalid choice. Try again.")

def save():
    pass

def main():
    set_up()

if __name__ == "__main__":
    main()