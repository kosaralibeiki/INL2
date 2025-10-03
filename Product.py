from datetime import datetime
from enum import Enum
#product_id, product_name, price, price_type
# check the privacy and _

class Product:
    def __init__(self, product_id, product_name, price, price_type ):
        self.product_id = product_id
        self.price = float(price)
        self.price_type = price_type
        self.product_name = str(product_name)

    def __str__(self):
        return f"{self.product_name} (ID: {self.product_id}) - {self.price} per {self.price_type}"

class Validation:
    @staticmethod
    def validate_product_price(price_prompt):
        try:
            price = float(input(price_prompt))
            if price < 0:
                print("🤔 Pris kan inte vara negativt!")
                return False
            return price
        except ValueError:
            print("🤔 Ogiltigt pris! Ange en siffra.")
            return False

    @staticmethod
    def validate_product_type(type_prompt):
        product_type = input(type_prompt).strip().lower()
        if product_type != "styck" and product_type != "kilo":
            print("🤔 Välj mellan styck eller kilo!!!")
            return False
        return True

    @staticmethod
    def get_valid_date(date_prompt):
        while True:
            date_str = input(date_prompt).strip()
            try:
                valid_date = datetime.strptime(date_str, "%d-%m")
                return valid_date
            except ValueError:
                print("🤔 Ogiltigt datum! Ange datum i formatet ÅÅÅÅ-MM-DD (t.ex. 2025-10-10).")

    @staticmethod
    def get_valid_campaign_date(start_date, end_date):
        if start_date >= end_date:
            print("Starttiden kan inte vara före sluttiden!")
            return False
        return True


class Products:
    def __init__(self):
        self.products:dict[str,Product]= {}

    def load_products(self):
        try:
            with open("all_products.txt", "r", encoding="utf-8") as f:
                next(f)
                for line in f:
                    product_id, product_name, price, price_type,  = line.strip().split(";")
                    self.products[product_id] = Product(product_id, product_name, price, price_type )
        except FileNotFoundError:
            print("😓 File not found!")

    def validate_product(self, product_id):
        product = self.products.get(product_id)
        if not product:
            print("Produkt-id finns ej")
            return None
        return product

    def validate_product_id(self, prompt):
        while True:
            product_id = input(prompt).strip()

            if not self.validate_product(product_id):
                print("Ogiltigt produkt-ID, försök igen.")
                return False
            else:
                return product_id

    def validate_product_name(self, prompt):
        while True:
            product_name = input(prompt).strip()

            for p in self.products.values():
                if p.product_name.lower() == product_name.lower():
                    print("Produktnamn finns redan i listan!")
                    return False

            if product_name.isdigit():
                print("Produktnamn kan inte enbart innehålla siffror!")
                return False

            return True

    def generate_product_id(self):
        if not self.products:
            return 1
        all_ids = [int(pro_id) for pro_id in self.products.keys()]
        new_id = max(all_ids) + 1
        return new_id

    @staticmethod
    def str_new_product(product_id, product_name, product_price, price_type):
        return f"{product_name} med produkt-ID:{product_id} och pris per {price_type}: {product_price} har lagt till!"

    def validate_new_name(self, product_id, new_name):
            if product_id not in self.products:
                print("Produkt-id finns ej")
                return False

            for pro in self.products.values():
                if pro.product_name.lower() == new_name.lower():
                    print(f"Namnet {new_name} finns redan i lista!")
                    return False

            self.products[product_id].product_name = new_name
            print(f"Produktens namn har ändrats till {new_name.capitalize()}.")
            return True

    def add_new_product(self):
        while True:
            while True:
                product_name = input("Produktnamn: ").strip().title()
                if not self.validate_product_name(product_name):
                    continue
                break

            while True:
                product_price = Validation.validate_product_price("Produktpris: ")
                if not product_price:
                    continue
                break

            while True:
                price_type = Validation.validate_product_type("Produkttyp (styck/kilo): ")
                if not price_type:
                    continue
                break


            product_id = str(self.generate_product_id())
            new_product = Product(product_id, product_name, product_price, price_type)
            self.products[product_id] = new_product

            print(self.str_new_product(product_id, product_name, product_price, price_type))
            break

    def change_product_name(self):
        while True:
            product_id = input("Ange produktens ID: ").strip()
            new_name = input("Ange produktens nytt namn: ").strip().capitalize()

            if not self.validate_new_name(product_id, new_name):
                continue



class PriceCampaigns:
    def __init__(self):
        self.campaigns: dict[str, {str, }] = {}

    def get_campaigns_info(self):
        for cam_info in self.campaigns.values():
            print(cam_info)

    def existing_campaigns(self):
        if not self.campaigns:
            print("Ingen Kampanjpris register annu!")
            return None

        for cam_id, cam_info in self.campaigns.items():
            print(f"{cam_id} - {cam_info['name']}")

    def get_valid_campaign_name(self, name_prompt):
        while True:
            campaign_name = input(name_prompt).strip()
            if campaign_name in self.get_campaigns_info():
                print(f"Ett kampanjpris med titel {campaign_name} finns redan i listan!")
                return False

            return True

    def get_valid_campaign_id(self, id_prompt):
        while True:
            campaign_id = input(id_prompt).strip()
            if campaign_id in self.campaigns.keys():
                print(f"Ett kampanjpris med ID {campaign_id} finns redan i listan!")
                return False
            return campaign_id


    def create_campaign(self, products: Products):
        while True:
            cam_name = self.get_valid_campaign_name("Kampanjnamn: ")
            if not cam_name:
                continue
            break

        while True:
            cam_id = self.get_valid_campaign_id("Kampanj-id: ")
            if not cam_id:
                continue
            break

        while True:
            new_price = Validation.validate_product_price("Produktpris: ")
            if not new_price:
                break
            continue

        while True:
            start_date = Validation.get_valid_date("Ange kampanjens startdatum (MM-DD):")
            end_date = Validation.get_valid_date("Ange kampanjens slutdatum  (MM-DD):")
            valid_date = Validation.get_valid_campaign_date(start_date, end_date)
            if not valid_date:
                continue
            break

        self.campaigns[cam_id] = {
            "name": cam_name,
            "products": products,
            "new_price": new_price,
            "start_date": start_date,
            "end_date": end_date,
        }

        print(f"Kampanjen '{cam_name}' (ID: {cam_id}) har lagts till!")


po = Products()
po.load_products()
po.add_new_product()
po.change_product_name()
