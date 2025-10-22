import json
from datetime import datetime

class Receipt:

    def __init__(self, receipt_no, products):
        self.receipt_no = receipt_no
        self.products = products

        self.header_added = False
        self.receipt = {
            "header" : {"date" : self.generate_rcp_date()},
            "lines" : [],
            "total" : 0
        }


# ---------- Header ----------
    @staticmethod
    def generate_rcp_date():
        """Date and time in Swedish format."""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    @staticmethod
    def str_rcp_date():
        return f"KVITTO\t{Receipt.generate_rcp_date()}"

    def add_rcp_header(self):
        self.receipt["header"]["date"] = self.str_rcp_date()
        self.header_added = True

    def print_rcp_header(self):
        return "INGEN DATUM" if not self.receipt["header"]["date"] else self.str_rcp_date()  # wondering why Kassa?


# ---------- Receipt body ----------
    @staticmethod
    def validate_command(command):
        if " " not in command:
            print("🤔 Ange mellanslag mellan produktid och antal!")
            return None

        parts = command.strip().split()
        if len(parts) != 2:
            print("🤔 Du måste skriva två värden: produkt-id och antal.")
            return None

        product_id, quantity = parts
        if not product_id.isdigit() or not quantity.isdigit():
            print("🤔 Fel! Produkt-id och antal måste vara siffror.")
            return None

        qty = int(quantity)
        if qty == 0:
            print("🤔 Fel! Antal måste vara större än noll.")
            return None

        return product_id, qty

    @staticmethod
    def one_line_total(product, quantity):
        return float(product.price) * int(quantity)

    def add_total_line(self, product, quantity):
        line_total = self.one_line_total(product, quantity)
        self.receipt['total'] += line_total
        return self.receipt["total"]

    def print_rcp_total(self):
        return f"Total: {self.receipt['total']:.2f}"

    def add_rcp_line(self, product, quantity):
        line = {
            "product_name": product.name,
            "quantity": quantity,
            "price": float(product.price),
            "line_total": self.one_line_total(product, quantity)
        }
        self.add_total_line(product, quantity)
        self.receipt["lines"].append(line)


    @staticmethod
    def product_line_str(line):
        return f"{line['product_name']}\t{line['quantity']} * {line['price']} = {line['line_total']:.2f}"

    def print_rcp_body(self):
        if not self.receipt["lines"]:
            return "Inga varor!"


        lines = [self.product_line_str(line) for line in self.receipt["lines"]]
        return "\n".join(lines)


    # ---------- Printing the receipt ----------
    def print_rcp(self):
        header = self.print_rcp_header()
        body = self.print_rcp_body()
        total = self.print_rcp_total()

        receipt_text = f"{header}\n{body}\n{total}"
        return receipt_text

    # ---------- Main logic ----------
    def new_receipt(self):

        print("kommandon:")
        print("<produktid> <antal>")
        print("PAY")

        while True:
            print()
            command = input("Kommando: ").strip()
            print()

            if command.upper() == "PAY":
                return self.print_rcp()

            valid_input = self.validate_command(command)
            if not valid_input:
                continue

            product_id, quantity = valid_input
            product = self.products.validate_product(product_id)

            if not product:
                continue

            self.add_rcp_line(product, quantity) #lines added

            print(self.print_rcp())



# ---------- Receipts manager ----------
class ManageReceipts:
    def __init__(self):
        self.receipts = {}
        self.receipt_no = 1000

    def generate_receipt_no(self):
        self.receipt_no += 1
        return self.receipt_no

    @staticmethod
    def generate_file_name():
        today = datetime.now().strftime("%Y%m%d")
        return f"receipt_{today}.json"

    # def load_day_receipts(self):
    #     try:
    #         with open(Receipts.generate_file_name(), "r") as f:
    #             data = json.load(f)
    #             for self.receipt_no, receipt in data.items():
    #                 self.receipts[self.receipt_no] = receipt
    #
    #     except FileNotFoundError:
    #         Receipts.generate_file_name()

    def save_receipt(self, receipt):
        file_name = self.generate_file_name()

        self.receipts[receipt.receipt_no] = receipt

        with open(file_name, "a", encoding="utf-8") as f:
            f.write(f"{self.receipt_no}: ")
            json.dump(receipt.receipt, f, ensure_ascii=False, indent=4)
            f.write(",\n")



            # def save_receipts(self, receipt_no):
    #     with open("receipts.txt" , "w") as f:



