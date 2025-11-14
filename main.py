from Product_module import Products, Product
from Receipt_module import Receipt, ManageReceipts
from Campaign_module import ManageCampaign



def set_up():
    products = Products()
    products.load_products()

    camps = ManageCampaign()
    camps.load_camps()

    for camp in camps.campaigns.values():
        camps.attach_campaign_to_products(camp, products)
    while True:
        print()
        print("KASSA")
        print("1. Ny kund")
        print("2. Admin")
        print("0. Avsluta")
        print()

        choice =input("Choose an option: ")
        print()

        # Ny kund
        if choice == "1":

            receipts_manager = ManageReceipts()
            receipt_no = receipts_manager.generate_receipt_no()

            receipt = Receipt(receipt_no, products=products, campaigns=camps)
            print(receipt.new_receipt())
            receipts_manager.save_daily_receipt(receipt)

        # Admin
        elif choice == "2":
            while True:
                print("1. Ändra på befintliga produkter")
                print("2. Lägg till en produkt")
                print("3. Lägg till en kampanjpris")
                print("4. Ta bort en kampanjpris")
                print("0. Tillbaka till menyn")


                choice_2 = input("Vad skulle du ändra på? ").strip()


                #Ändra på befintliga produkter
                if choice_2 == "1":
                    product = products.find_product_by_id()
                    print(product)
                    print()
                    print("1. Namn")
                    print("2. Pris")
                    print("0. Avbryt")

                    choice_3 = input("Vad vill du ändra?")
                    print()


                    # Ändra på produktnamn
                    if choice_3 == "1":
                        products.change_product_name(product)
                        break

                    # Ändra på produktpris
                    elif choice_3 == "2":
                        products.change_product_price(product)
                        break

                    elif choice_3 == "0":
                        break

                    else:
                        print("Invalid input!")
                        continue


                # Lägg till en produkt
                elif choice_2 == "2":
                    products.add_new_product()
                    products.save_products()

                # Lägg till en kampanjpris
                elif choice_2 == "3":
                    camps.create_campaign(products)
                    camps.save_camps()

                # Ta bort en kampanjpris
                elif choice_2 == "4":
                    camps.remove_campaign()
                    camps.save_camps()

                # Tillbaka till menyn
                elif choice_2 == "0":
                    break

                else:
                    print("Invalid choice. Try again.")

        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

def save():
    pass

def main():
    set_up()

if __name__ == "__main__":
    main()