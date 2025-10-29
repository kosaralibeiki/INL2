from Product_module import Product, Products
from datetime import datetime
import json

class Campaign:
    def __init__(self, camp_id:str, name:str, start_date:datetime, end_date:datetime, products:list[dict]):
        self.camp_id = camp_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.products = products



    def __str__(self):
        products_str ="\n".join([f" - produkt-id: {p['product_id']}, produktpris: {p['price']}kr"
                                 for p in self.products]
                                )
        return (
            f"\n🆔 Kampanj-ID: {self.camp_id}\n"
            f"📛 Namn: {self.name}\n"
            f"📅 Period: {self.start_date.strftime('%Y-%m-%d')} → {self.end_date.strftime('%Y-%m-%d')}\n"
            f"🧾 Produkter:\n{products_str}"
        )

    def to_dict(self) -> dict:
        return {
            "camp_id": self.camp_id,
            "name": self.name,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "products": self.products
        }



class ManageCampaign:
    def __init__(self):
        self.campaigns: dict[str, Campaign] = {}

    def load_camps(self):
        try:
            with open("Kompanipriser.json", "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for camp_id, camp_dict in json_data.items():
                    start_date = datetime.strptime(camp_dict["start_date"], "%Y-%m-%d")
                    end_date = datetime.strptime(camp_dict["end_date"], "%Y-%m-%d")
                    self.campaigns[camp_id] = Campaign(
                        camp_id=camp_id,
                        name=camp_dict["name"],
                        start_date=start_date,
                        end_date=end_date,
                        products=camp_dict["products"]
                    )
        except FileNotFoundError:
            self.campaigns = {}

    def save_camps(self):
        with open("Kompanipriser.json", "w", encoding="utf-8") as f:
            json.dump({cid: camp.to_dict() for cid, camp in self.campaigns.items()},
                      f, indent=4)

    def create_campaign(self, products : Products):

        while True:
            camp_name = self.get_camp_name()

            start_date = self.get_valid_date("Startdatum(ÅÅÅÅ-MM-DD): ")
            end_date = self.get_valid_date("Slutdatum(ÅÅÅÅ-MM-DD): ")
            if not self.get_valid_campaign_date(start_date, end_date):
                continue

            print("\n🛒 Lägg till produkter i kampanjen.")
            print("Skriv produkt-ID och kampanjpris. \n")


            #ask the id to get the product

            campaign_products = []
            while True:
                product_ = products.find_product_by_id() #find the product
                if not product_:
                    continue


                print(f"Produktnamn är {product_.name}")
                print(f"Nuvarande pris: {product_.price:.2f} kr per {product_.price_type}")
                camp_price = products.get_product_price("Nytt pris: ")

                if camp_price >= product_.price:
                    print("⚠️ Kampanjpriset måste vara lägre än ordinarie pris.")
                    continue

                campaign_products.append({
                    "id": product_.id_,
                    "price": camp_price
                })

                more = input("Lägga till fler produkter? (j/n): ").strip().lower()
                if more != "j":
                    break

            camp_id = str(len(self.campaigns) + 1)

            new_campaign = Campaign(camp_id = camp_id,
                                    name = camp_name,
                                    start_date = start_date,
                                    end_date = end_date,
                                    products = campaign_products)

            self.campaigns[camp_id] = new_campaign


            print(f"\n✅ Kampanjen '{camp_name}' skapades med {len(campaign_products)} produkter!\n")
            break


    @staticmethod
    def attach_campaign_to_products(campaign ,products : Products):
        """Links a campaign to the actual Product instances."""
        for item in campaign.products:
            product_obj = products.get_product(item["id"])
            if product_obj:
                product_obj.campaigns.append(campaign)

    def see_all_campaign(self):
        if not self.campaigns:
            print("🤔 Inga kampanjer finns ännu!")
            return

        for camp_id, camp in self.campaigns.items():
            print("-" * 30)
            print(camp)
            print("-" * 30)

    def remove_campaign(self):
        campaign_id = input("kampanjpris-id: ").strip()

        if campaign_id not in self.campaigns:
            print(f"❌ Ingen kampanj med ID {campaign_id} hittades!")
            return

        confirm = input(f"Är du säker att du vill ta bort kampanj {campaign_id}? (j/n): ").strip().lower()
        if confirm == "j":
            del self.campaigns[campaign_id]
            print(f"🗑️ Kampanj {campaign_id} har tagits bort.")
        else:
            print("❎ Åtgärden avbröts.")





    def get_camp_name(self):
        while True:
            new_name = input("Kampanjpris namn: ").strip()

            if not new_name:
                print("⚠️ Ange ett namn, det får inte vara tomt.")
                continue


            for campaign in self.campaigns.values():
                if campaign.name.lower() == new_name.lower():
                    print(f"❌ Namnet '{new_name}' är redan taget.")
                    break
            else:
                return new_name

    @staticmethod
    def get_valid_date(date_prompt):
        while True:
            date_str = input(date_prompt).strip()
            try:
                valid_date = datetime.strptime(date_str, "%Y-%m-%d")
                return valid_date
            except ValueError:
                print("🤔 Ogiltigt datum! Ange datum i formatet ÅÅÅÅ-MM-DD (t.ex. 2025-10-10).")

    @staticmethod
    def get_valid_campaign_date(start_date, end_date):
        if start_date >= end_date:
            print("Starttiden kan inte vara före sluttiden!")
            return False
        return True



