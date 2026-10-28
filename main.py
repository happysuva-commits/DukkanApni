
import json
import os

# Load products from file
if os.path.exists("products.json"):
    with open("products.json", "r") as f:
        products = json.load(f)
    
else:
    products = [
        {"name": "Rice", "price": 60, "quantity": 10},
        {"name": "Milk", "price": 30, "quantity": 5},
        {"name": "Sugar", "price": 45, "quantity": 8}
    ]

# Load sales data from file
if os.path.exists("sales.json"):
    with open("sales.json", "r") as f:
        sales_data = json.load(f)

    total_sales = sales_data["total_sales"]
    total_items_sold = sales_data["total_items_sold"]
else:
    total_sales = 0
    total_items_sold = 0


#save sales to json file
def save_sales():
    sales_data = {
        "total_sales": total_sales,
        "total_items_sold": total_items_sold
    }

    with open("sales.json", "w") as f:
        json.dump(sales_data, f, indent=4)

#reset function
def reset_sales():
    global total_sales,total_items_sold # global thi function bar na variable add kari sake

    total_sales = 0
    total_items_sold = 0

    save_sales()
    print("Sales report reset successfully!")



# Save products to JSON file
def save_products():
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)


# Main menu
while True:
    print("\n========================")
    print("      DUKKANAPNI")
    print("========================")
    print("1. Add Product")
    print("2. View Products")
    print("3. Search Product")
    print("4. Generate Bill")
    print("5. Sales Report")
    print("6. Reset sales report")
    print("7. Exit")
    print("========================")

    choice = input("Enter a choice: ")

    # Add Product
    if choice == "1":
        name = input("Enter product name: ").strip() #space remove karva
        #duplicate same product sae bachva
        if any(p["name"].lower() == name.lower() for p in products):
            print("Product already exists!")
            #ano matlb current loop muki farii menu ma jav
            continue
        try:
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))

            if price <= 0 or quantity <= 0:
                print("Price and quantity must be positive!")
                #a product add karya vagar menu par pacha jav
                continue
            
            # Product ni details dictionary ma store karo
            
            new_product = {
                "name": name,
                "price": price,
                "quantity": quantity
            }
            #navo product list ma add karva
            products.append(new_product)
            save_products() #update product json ma save karva

            print("Product added successfully!")
        #qunty ma invalid  no nakhe to error 
        except ValueError:
            print("Please enter valid numbers!")

    # View Products
    elif choice == "2":
        if not products:
            print("No products available!")
        else:
            for product in products:
                print("------------------------")
                print("Name:", product["name"])
                print("Price: Rs.", product["price"])
                print("Quantity:", product["quantity"])

    # Search Product
    elif choice == "3":
        search_name = input("Enter product name to search: ")
        found = False

        for product in products:
            if product["name"].lower() == search_name.lower():
                print("\nProduct Found!")
                print("Name:", product["name"])
                print("Price: Rs.", product["price"])
                print("Quantity:", product["quantity"])
                found = True
                break

        if not found:
            print("Product not found!")

    # Generate Bill
    elif choice == "4":
        bill_name = input("Enter product name: ")
        found = False

        try:
            bill_quantity = int(input("Enter quantity: "))

            for product in products:
                if product["name"].lower() == bill_name.lower():
                    found = True

                    if 0 < bill_quantity <= product["quantity"]:
                        total = product["price"] * bill_quantity

                        print("\n======= CUSTOMER BILL =======")
                        print("Product:", product["name"])
                        print("Price: Rs.", product["price"])
                        print("Quantity:", bill_quantity)
                        print("Total Bill: Rs.", round(total, 2))

                        # Update sales
                        total_sales += total
                        total_items_sold += bill_quantity
                        #save sales parmanently
                        save_sales()

                        # Update and save stock
                        product["quantity"] -= bill_quantity
                        #save product parmanently
                        save_products()

                        print("Remaining stock:", product["quantity"])
                        print("=============================")

                    else:
                        print("Invalid quantity or insufficient stock!")

                    break

            if not found:
                print("Product not found!")

        except ValueError:
            print("Please enter a valid whole-number quantity!")

    # Sales Report
    elif choice == "5":
        print("\n======= SALES REPORT =======")
        print("Total Sales: Rs.", round(total_sales, 2))
        print("Total Items Sold:", total_items_sold)
        print("============================")

    # Reset sales
    elif choice == "6":
        confirm = input("Reset sales report? (yes/no): ")

        if confirm.lower() == "yes":
            reset_sales()
        else:
            print("Reset cancelled!")

    # exit
    elif choice =="7":
        print("Thank you for using DukkanApni!")
        break

# invalid
    else:
        print("Invalid choice! Please select 1 to 6.")
