from datetime import datetime


class Product:
    def __init__(self, id_:str, name:str, price:float, price_type:str)-> None:
        self.id_ = id_
        self.price = price
        self.price_type = price_type
        self.name = name
        self.campaigns:list["Campaign"] = []



    def __str__(self)-> str:
        return f"ID: {self.id_}\nNamn: {self.name}\nPris per {self.price_type} : {self.price:.2f}"

    @property
    def current_price(self) -> float:
        today = datetime.now().date()
        active_prices = []

        for campaign in self.campaigns:
            if campaign.start_date.date() <= today <= campaign.end_date.date():
                for item in campaign.products:
                    if item["id"] == self.id_:
                        active_prices.append(item["price"])


        return min(active_prices) if active_prices else self.price



class Products:
    def __init__(self) -> None:
        self.products:dict[str,Product] = {}

    def load_products(self) -> None:
        try:
            with open("all_products.txt", "r", encoding="utf-8") as f:
                next(f)
                for line in f:
                    product_id, product_name, product_price, price_type = line.strip().split(";")
                    self.products[product_id] = Product(product_id, product_name, float(product_price), price_type )
        except FileNotFoundError:
            print("😓 File not found!")

    def save_products(self) -> None:
        with open("all_products.txt", "w", encoding="utf-8") as f:
            f.write("id;name;price;price_type\n")

            for pro in self.products.values():
                f.write(f"{pro.id_};{pro.name};{pro.price};{pro.price_type}\n")

    def add_new_product(self):
        while True:
            name_ = self.get_product_name()
            price_ = self.get_product_price("Pris: ")
            price_type_ = self.valid_product_price_type()
            id_ = str(self.generate_product_id())

            new_product = Product(id_=id_, name=name_, price=price_, price_type=price_type_)
            self.products[id_] = new_product

            print("✅ Ny produkt tillagd:")
            print(new_product)


            self.save_products()
            break

    def change_product_name(self, product_) -> None:
        new_name = self.get_product_name()
        product_.name = new_name
        print(f"✅ Produkten med produkt-id {product_.id_} ändrades namn till {new_name}")
        self.save_products()

    def change_product_price(self, product_) -> None:
        while True:
            new_price =self.get_product_price("Nytt pris:")

            if new_price == product_.price:
                print("❌ Det nya priset är samma som det gamla.")
                continue

            product_.price = new_price
            print(f"✅ Produkten med ID {product_.id_} ändrades pris till {new_price:.2f} kr per {product_.price_type}.")
            break

        self.save_products()



    def find_product_by_id(self) -> Product | None:
        """The method asks for id and returns the product"""
        while True:
            product_id = input("Product ID: ").strip()
            product_ = self.products.get(product_id)

            if not product_:
                print("❌ Produkt-ID finns inte! Försök igen.")
                continue
            else:
                print("✅ En produkt hittades:")
                return product_

    def get_product(self, product_id:str) -> Product | bool:
        product_ = self.products.get(product_id)
        if not product_:
            print("❌ Produkt-ID finns inte! Försök igen.")
            return False
        else:
            # print("✅ En produkt hittades:")
            return product_


    @staticmethod
    def get_product_price(prompt:str) -> float | None:
        while True:
            price_ = input(prompt).strip()
            try:
                price_ = float(price_)

                if price_ <= 0:
                    print("❌ Priset måste vara större än 0.")
                    continue

                return price_

            except ValueError:
                print("❌ Ogiltigt pris! Ange ett numeriskt värde (t.ex. 12.50).")
                continue

    def get_product_name(self) -> str | None:
        while True:
            new_name = input("Nytt namn: ").strip().title()

            for prod in self.products.values():
                if new_name.lower() == prod.name.lower():
                    print(f"❌ Produkten '{new_name}' finns redan!")
                    break
            else:
                return new_name

    @staticmethod
    def valid_product_price_type()-> str | None:
        while True:
            product_type = input("Produkt-typ (styck/kilo): ").strip().lower()

            if product_type != "styck" and product_type != "kilo":
                print("❌ Välj mellan 'kilo' eller 'styck'! ")
                continue

            return product_type

    def generate_product_id(self) -> str:
        if not self.products:
            return str(1)
        all_ids = [int(pro_id) for pro_id in self.products.keys()]
        new_id = max(all_ids) + 1
        return str(new_id)







