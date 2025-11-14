import json
from datetime import datetime

from Campaign_module import Campaign, ManageCampaign
from Product_module import Products



class Receipt:

    def __init__(self, receipt_no:str, products:Products, campaigns:ManageCampaign):
        self.receipt_no = receipt_no
        self.products = products
        self.campaigns = campaigns

        self.header_added = False
        self.receipt:dict[str, dict | list | int] = {
            "header" : {"date" : self.generate_rcp_date()},
            "lines" : [],
            "total" : 0
        }


    def new_receipt(self):

        print("kommandon:")
        print("<produktid> <antal>")
        print("PAY")

        while True:
            print()
            command = input("Kommando: ").strip()
            print()

            if command == "PAY":
                return self.attach_receipt_parts()

            valid_input = self.validate_command(command)
            if not valid_input:
                continue

            product_id, quantity = valid_input
            product = self.products.get_product(product_id)

            if not product:
                continue

            self.create_receipt_line(product, quantity)

            print(self.attach_receipt_parts())

    def attach_receipt_parts(self) -> str:
        header = self.str_rcp_header()
        body = self.attach_receipt_body()
        total = self.str_receipt_total()

        receipt_text = f"{header}\n{body}\n{total}"
        return receipt_text




    @staticmethod
    def generate_rcp_date() -> str:
        """Date and time in Swedish format."""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    @staticmethod
    def str_rcp_date() -> str:
        return f"KVITTO\t{Receipt.generate_rcp_date()}"

    def attach_rcp_header(self) -> None:
        self.receipt["header"]["date"] = self.str_rcp_date()
        self.header_added = True

    def str_rcp_header(self)-> str:
        return "INGEN DATUM" if not self.receipt["header"]["date"] else self.str_rcp_date()




    @staticmethod
    def validate_command(command:str) -> tuple[str, int] | None:
        """To make sure user follow the rules related to command"""

        if " " not in command:
            print("❌ Ange mellanslag mellan produktid och antal!")
            return None

        parts = command.strip().split()
        if len(parts) != 2:
            print("❌ Du måste skriva två värden: produkt-id och antal.")
            return None

        product_id, quantity = parts
        if not product_id.isdigit() or not quantity.isdigit():
            print("❌ Fel! Produkt-id och antal måste vara siffror.")
            return None

        qty = int(quantity)
        if qty == 0:
            print("❌ Fel! Antal måste vara större än noll.")
            return None

        return product_id, qty

    @staticmethod
    def get_line_total(product, quantity) -> float:
        """Calculate the total price for a single product line"""
        return product.current_price * int(quantity)

    def update_receipt_total(self, product, quantity)-> float:
        line_total = self.get_line_total(product, quantity)
        self.receipt['total'] += line_total
        return self.receipt["total"]

    def str_receipt_total(self)-> str:
        return f"Total: {self.receipt['total']:.2f}"



    def create_receipt_line(self, product, quantity):
        line = {
            "product_name": product.name,
            "quantity": quantity,
            "price": float(product.current_price),
            "line_total": self.get_line_total(product, quantity)
        }
        self.update_receipt_total(product, quantity)
        self.receipt["lines"].append(line)

    @staticmethod
    def product_line_str(line)-> str:
        return f"{line['product_name']}\t{line['quantity']} * {line['price']} = {line['line_total']:.2f}"

    def attach_receipt_body(self) -> str:
        if not self.receipt["lines"]:
            return "Inga varor!"

        lines = [self.product_line_str(line) for line in self.receipt["lines"]]
        return "\n".join(lines)






# ---------- Receipts manager ----------
class ManageReceipts:
    def __init__(self):
        self.receipts: dict[int, dict] = {}
        self.receipt_no: int = 1000

    def generate_receipt_no(self):
        self.receipt_no += 1
        return self.receipt_no

    @staticmethod
    def generate_file_name()-> str:
        today = datetime.now().strftime("%Y%m%d")
        return f"receipt_{today}.json"

    def save_daily_receipt(self, receipt):
        file_name = self.generate_file_name()

        self.receipts[receipt.receipt_no] = receipt

        with open(file_name, "a", encoding="utf-8") as f:
            f.write(f"{self.receipt_no}: ")
            json.dump(receipt.receipt, f, ensure_ascii=False, indent=4)
            f.write(",\n")






