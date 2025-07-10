from datetime import datetime

products_file_path = "products.txt"
orders_file_path = "orders.txt"
supplier_orders_file = "supplier_orders.txt"
supplier_file = "suppliers.txt"

#UTILITY METHODS
def read_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            items = file.readlines()
            for i in range(len(items)):
                items[i] = items[i].strip()
            return items
    except FileNotFoundError:
        # Create the file if it doesn't exist
        with open(file_path, "w"):
            return []

def save_to_file(items, file_path):
    # Write updated orders back to the file
    try:
        with open(file_path, "w") as file:
            for item in items:
                file.write(item + "\n")
            return True
    except IOError:
        print(f"Error: Couldn't save to {file_path}")
        return False

def print_products(product_list):
    print_product_header()
    for product in product_list:
        print(product_to_string(product))

def print_product_header():
    print(f"{'Product ID':<12}{'Name':<20}{'Description':<30}{'Price':<10}{'Stock':<10}")
    print("-" * 80)

def get_item_details(item):
    return item.strip().split(";")

def get_item_from_details(item_details):
    item = ""
    for i in range(len(item_details)):
        item = item + ";" + str(item_details[i])
    return item[1:]

def product_to_string(product):
    details = get_item_details(product)
    return f"{details[0][:11]:<12}{details[1][:19]:<20}{details[2][:29]:<30}{details[3][:9]:<10}{details[4][:9]:<10}"

def parse_int(value, error_message):
    try:
        return int(value)
    except ValueError:
        if error_message != "":
            print(error_message)
        return 0

def get_item_index_from_id(item_id, file_path):
    items = read_from_file(file_path)
    for i in range(len(items)):
        details = get_item_details(items[i])
        if details[0] == item_id:
            return i

    return -1

def generate_next_id(file_path):
    items = read_from_file(file_path)
    if not items:
        return 0

    last_id = get_item_details(items[-1])[0]
    next_id = parse_int(last_id, f"Error: Invalid ID {last_id} found in {file_path}") + 1

    # ensure no duplicate order ids occur
    cont = True
    while cont:
        cont = False
        for item in items:
            if str(next_id) == get_item_details(item)[0]:
                next_id += 1
                cont = True
                break

    return next_id

def print_suppliers():
    suppliers = read_from_file(supplier_file)
    # if there are no suppliers, we can't show any
    if len(suppliers) == 0:
        print("No suppliers found")
        return

    print(f"{'Supplier ID':<12}{'Name':<20}{'Contact Number':<20}")
    print("-" * 55)
    for supplier in suppliers:
        details = get_item_details(supplier)
        print(f"{details[0][:11]:<12}{details[1][:19]:<20}{details[2][:19]:<20}")

def input_and_validate_product_id():
    # Code will loop until the correct product id format is entered
    while True:
        product_id = input("Enter Product ID (Format : PXXX, X = digit): ")
        if len(product_id) != 4 or not product_id.startswith("P") or not product_id[1:4].isdigit():
            print("Wrong Product ID Format, Try Again")
        else:
            # Check for duplication of products
            if get_item_index_from_id(product_id, products_file_path) != -1:
                print("This Product Has Already Been Added To The Database")
                continue
            else:
                break
    return product_id

def input_product_name():
    # Code will loop until a product name is entered
    while True:
        product_name = input("Enter Product Name: ")

        if not product_name.strip():
            print("Please Enter A Product Name")
        else:
            break
    return product_name

def input_product_quantity():
    # Code will loop until user enters an Integer for quantity
    while True:
        try:
            inventory = int(input("Enter The Quantity Of Product Available: ").strip())
        except ValueError:
            print("Please enter a whole number")
            continue

        # Provides flexibility to add products despite having 0 stock
        # while also validating the stock level to not be negative
        if inventory >= 0:
            return inventory
    return 0


def input_product_price():
    # Code will loop until user enters a floating number for the product
    while True:
        price = input("Enter Product Price: RM ")

        if not price.strip():
            print("Please enter price as a number")
        else:
            try:
                # we ensure it is a float, but we don't convert price to float because it will be
                # stored as a string anyway
                float(price)
                break
            except ValueError:
                print("Please Make Sure You Entered The Price And Not Something Else")
    return price


def input_product_description():
    # Code will loop until a product description is entered
    while True:
        description = input("Enter Product Description: ")

        if not description.strip():
            print("Please Enter A Description For The Product")
        else:
            break
    return description

#MENUS
def update_product():
    # Check if the file exists
    product_list = read_from_file(products_file_path)

    # if there are no products, we can't update any
    if len(product_list) == 0:
        print("No products found to update.")
        return

    # Update products sub-menu
    while True:
        print("Update Products:")
        print("1. Show available products")
        print("2. Choose product to update")
        print("3. Back to main menu")

        option = input("Enter your choice: ")
        if option == "1":
            view_inventory()
        elif option == "2":
            print("Available Products:")
            print_product_header()
            i = 1
            for product in product_list:
                print(f"{i}. {product_to_string(product)}")
                i += 1

            user_input = input("\nEnter the number of the product to update: ")
            choice = parse_int(user_input, "Invalid input. Please enter a number.")
            if choice < 1 or choice > len(product_list):
                print("Invalid choice.")
                continue

            # Split the selected product's details
            selected_product = get_item_details(product_list[choice - 1])
            print("Current Details:")
            print(f"1. Product ID: {selected_product[0]}")
            print(f"2. Name: {selected_product[1]}")
            print(f"3. Description: {selected_product[2]}")
            print(f"4. Price: {selected_product[3]}")
            print(f"5. Quantity: {selected_product[4]}")
            print("6. Back")

            # Let the user select the detail to be updated
            try:
                user_input = input("Enter your choice: ")
                detail_to_update = int(user_input)
                if detail_to_update == 6:
                    continue

                if detail_to_update < 1 or detail_to_update > 5:
                    print("Invalid choice.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            # Lets the user enter the new value to be stored for that detail
            match detail_to_update:
                case 1:
                    selected_product[0] = input_and_validate_product_id()
                case 2:
                    selected_product[1] = input_product_name()
                case 3:
                    selected_product[2] = input_product_description()
                case 4:
                    selected_product[3] = input_product_price()
                case 5:
                    selected_product[4] = input_product_quantity()

            # Update and store the product details
            product_list[choice - 1] = get_item_from_details(selected_product)
            save_to_file(product_list, products_file_path)
            print("Product updated successfully.")
        elif option == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def view_inventory():
    product_list = read_from_file(products_file_path)
    if len(product_list) == 0:
        print("No products to display")
    else:
        print_products(product_list)

def generate_reports():
    while True:
        print("Generate Reports:")
        print("1. Low Stock Items")
        print("2. Product Sales")
        print("3. Supplier Orders")
        print("4. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            threshold = int(input("Enter the low stock threshold: "))
            print("Low Stock Items:")

            print_product_header()
            product_list = read_from_file(products_file_path)

            for product in product_list:
                product_details = get_item_details(product)
                stock = parse_int(product_details[4], f"Error: Incorrect value for stock at {product}")
                if stock < threshold:
                    print(product_to_string(product))
        elif choice == "2":
            print("Product Sales:")
            print(f"{'Order ID':<10}{'Product ID':<12}{'Quantity':<10}{'Order Date':<20}")
            print("-" * 55)
            orders = read_from_file(orders_file_path)
            for order in orders:
                details = get_item_details(order)
                print(f"{details[0][:9]:<10}{details[1][:11]:<12}{details[2][:9]:<10}{details[3][:19]:<20}")
        elif choice == "3":
            print("Supplier Orders:")
            print(f"{'Order ID':<10}{'Supplier ID':<12}{'Product ID':<12}{'Quantity':<10}{'Order Date':<20}")
            print("-" * 65)
            supplier_orders = read_from_file(supplier_orders_file)
            for order in supplier_orders:
                details = get_item_details(order)
                print(f"{details[0][:9]:<10}{details[1][:11]:<12}{details[2][:11]:<12}{details[3][:9]:<10}{details[4][:19]:<20}")

        elif choice == "4":
            break
        else:
            print("Invalid option.")

#add a new product and avoid duplication of product codes
def add_product():
    product_id = input_and_validate_product_id()
    product_name = input_product_name()
    description = input_product_description()
    price = input_product_price()
    inventory = input_product_quantity()

    #Adding the product into the database
    products = read_from_file(products_file_path)
    products.append(get_item_from_details([product_id, product_name, description, price, str(inventory)]))
    save_to_file(products, products_file_path)

def supplier_menu():
    # giving the user the option to either view, add supplier or return back to the main page
    while True:
        print("\nSupplier Menu:")
        print("1. View Supplier List")
        print("2. Add a New Supplier")
        print("3. Back to main menu")

        choice = input("Please choose an option (1, 2 or 3): ")

        # to view the current list of suppliers
        if choice == "1":
            print_suppliers()

        # to add a new supplier into the system
        elif choice == "2":
            # to make sure the supplier id format is correct
            while True:
                supplier_id = input("Please Enter the Supplier ID (Format: S0XX): ")
                if len(supplier_id) != 4 or not supplier_id.startswith('S0') or not supplier_id[2:4].isdigit():
                    print("Error: Supplier ID must be in the format 'S0XX' (e.g., S001). Try again.")
                else:
                    break

            supplier_name = input("Please Enter the Supplier Name: ")
            supplier_contact = input("Please Enter the Contact Information of the Supplier: ")

            # to make sure user did not enter blank spaces
            if not supplier_name.strip() or not supplier_contact.strip():
                print("Error: All fields must be filled.")
                continue

            # to check for duplicates that already exist in file
            duplicate_found = False
            suppliers = read_from_file(supplier_file)
            for supplier in suppliers:
                details = get_item_details(supplier)
                if details[0] == supplier_id:
                    duplicate_found = True
                    break

            if duplicate_found:
                continue

            # to append supplier information if no errors
            new_supplier = get_item_from_details([supplier_id, supplier_name, supplier_contact])
            suppliers.append(new_supplier)
            if save_to_file(suppliers, supplier_file):
                print("Supplier added successfully.")

            # to print the current list of suppliers
            print("\nCurrent List of Suppliers:")
            print_suppliers()
        elif choice == "3":
            print("Returning Back to Main Menu")
            return

        # in case user presses an invalid option to prevent error
        else:
            print("Invalid option. Please try again.")

def order_menu():
      while True:
        print("Order Menu:")
        print("1. Buy a product as a customer")
        print("2. Order products from suppliers")
        print("3. Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            customer_menu()
        elif choice == "2":
            supplier_order_menu()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def customer_menu():
    orders = read_from_file(orders_file_path)
    while True:
        print("\nCustomer Menu:")
        print("1. View Product List")
        print("2. Place an Order")
        print("3. Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Display the product catalog
            view_inventory()
        elif choice == "2":
            order_id = generate_next_id(orders_file_path)

            product_id = input("Enter Product ID: ")
            products = read_from_file(products_file_path)
            product_index = get_item_index_from_id(product_id, products_file_path)
            if product_index == -1:
                print("Invalid Product ID.")
                continue

            product = products[product_index]
            product_details = get_item_details(product)
            stock = parse_int(product_details[4], f"Error: Incorrect value for stock at {product}")
            if stock <= 0:
                print("No Stock available")
                continue

            while True:
                quantity = input("Enter Quantity (or type 'exit' to go back): ")
                if quantity == "exit":
                    return

                quantity = parse_int(quantity, "Invalid quantity. Please enter again")
                if quantity <= 0:
                    continue

                if quantity > stock:
                    print("Not enough stock available to complete this order")
                    continue

                order_date = str(datetime.now())[:19]
                order = get_item_from_details([order_id, product_id, quantity, order_date])
                orders.append(order)
                save_to_file(orders, orders_file_path)


                product_details[4] = str(stock - quantity)
                products[product_index] = get_item_from_details(product_details)
                save_to_file(products, products_file_path)
                print("Order added successfully.")
                break
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")

def supplier_order_menu():
    while True:
        print("\nSupplier Menu:")
        print("1. View Suppliers")
        print("2. Order Products from Supplier")
        print("3. Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            print_suppliers()
        elif choice == "2":

            supplier_id = input("Enter Supplier ID: ")


            index = get_item_index_from_id(supplier_id, supplier_file)
            if index == -1:
                print("Error: Invalid Supplier ID.")
                return


            product_id = input("Enter Product ID to restock: ")
            product_index = get_item_index_from_id(product_id, products_file_path)
            if product_index == -1:
                print("Error: Invalid Product ID.")
                return

            quantity = parse_int(input("Enter Quantity to Order: ").strip(), "Invalid quantity. Please enter again.")
            if quantity <= 0:
                print("Quantity must be greater than 0.")
                return


            supplier_order_id = generate_next_id(supplier_orders_file)
            order_date = str(datetime.now())[:19]
            supplier_orders = read_from_file(supplier_orders_file)
            supplier_order = get_item_from_details([supplier_order_id, supplier_id, product_id, quantity, order_date])
            supplier_orders.append(supplier_order)
            save_to_file(supplier_orders, supplier_orders_file)


            products = read_from_file(products_file_path)
            product_details = get_item_details(products[product_index])
            product_details[4] = str(int(product_details[4]) + quantity)
            products[product_index] = get_item_from_details(product_details)
            save_to_file(products, products_file_path)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("\nInventory Management System")
        print("1. Add a new product")
        print("2. Update product details")
        print("3. Add a new supplier")
        print("4. Place an order")
        print("5. View inventory")
        print("6. Generate reports")
        print("7. Exit")

        option = input("Enter your choice: ")
        match option:
            case "1":
                add_product()
            case "2":
                update_product()
            case "3":
                supplier_menu()
            case "4":
                order_menu()
            case "5":
                view_inventory()
            case "6":
                generate_reports()
            case "7":
                print("Exited program.")
                break
            case _:
                print("Invalid choice. Please enter a number from 1 to 7.")

main()
