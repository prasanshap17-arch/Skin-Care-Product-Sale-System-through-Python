# Importing necessary functions from other modules.
# - `load_products`: loads the current inventory from storage.
# - `save_products`: updates the product list in storage after changes.
# - `generate_invoice`: creates a sales or restock invoice for record-keeping.
from read import load_products
from write import save_products, generate_invoice


# Utility function to prompt user for a positive number input (integer or float).
# This function ensures that invalid entries, negative numbers, or zero are not accepted.
def get_positive_number(prompt, is_float=False):
    while True:
        try:
            value = input(prompt)
            # Convert input to float if required, else to int.
            if is_float:
                num = float(value)
            else:
                num = int(value)

            # Reject non-positive values.
            if num <= 0:
                print("Please enter a positive number")
                continue
            return num
        except ValueError:
            # Handle invalid (non-numeric) input.
            print("Invalid input. Please enter a valid number")


# Function to handle the sale of products to a customer.
# Implements "Buy 3 Get 1 Free" logic and charges customers 200% of the cost price.
def process_sale():
    try:
        # Load current product inventory
        products = load_products()
        if not products:
            print("No products available for sale")
            return

        print("\n" + " New Sale ".center(40, '═'))

        # Capture and sanitize customer name input
        customer = ' '.join(input("Customer Name: ").split())

        items = []  # List to store all products involved in the current sale
        total = 0   # Running total for the sale invoice

        # Loop for selecting multiple products
        while True:
            # Accept product ID or name. Typing 'done' exits the loop.
            product_input = ' '.join(input("\nEnter product ID/name (or 'done'): ").split()).lower()
            if product_input == 'done':
                break

            # Attempt to match product either by ID (numeric input) or by name.
            product = None
            if product_input.isdigit():
                product = next((p for p in products if p['id'] == int(product_input)), None)
            else:
                product = next((p for p in products if p['name'].lower() == product_input), None)

            # If product not found, show error and restart loop
            if not product:
                print("Product not found")
                continue

            # Display product details for confirmation
            print(f"Selected: {product['name']} ({product['brand']}) | Stock: {product['quantity']}")

            # Prompt for quantity to purchase
            qty = get_positive_number("Quantity to purchase: ")

            # Calculate number of free units using offer (e.g., 1 free per 3 bought)
            free = qty // 3

            # Check if total quantity needed (purchased + free) is available in stock
            if product['quantity'] < (qty + free):
                print(f"Insufficient stock. Available: {product['quantity']} (Need {qty + free})")
                continue

            # Deduct total (purchased + free) from available stock
            product['quantity'] -= (qty + free)

            # Selling price is fixed at 200% of cost price as per business policy
            price = product['price'] * 2

            # Add product details to the invoice
            items.append({
                'name': product['name'],
                'qty': qty,
                'free': free,
                'total': qty * price
            })
            total += qty * price

            print(f"Added {qty} units (+{free} free) of {product['name']}")

        # Finalize sale if at least one item was purchased
        if items:
            # Generate and save invoice
            invoice = generate_invoice(customer, items, total, "sale")
            save_products(products)  # Update stock in persistent storage

            print("\n" + " Sale Complete ".center(40, '═'))
            print(f"Invoice generated: {invoice}")
        else:
            print("Sale canceled - no items added")

    except Exception as e:
        # Catch unexpected errors for graceful failure
        print(f"Sale error: {e}")


# Function to handle restocking of products from a vendor.
# It can either increase quantity of existing products or create a new product.
def process_restock():
    try:
        # Load current products from storage
        products = load_products()

        print("\n" + " Restock Products ".center(40, '═'))

        # Input and clean vendor name
        vendor = ' '.join(input("Vendor Name: ").split())

        # Prompt user to enter a product ID or name to restock
        product_input = ' '.join(input("\nEnter product ID/name: ").split()).lower()
        if not product_input:
            print("Product name cannot be empty")
            return

        # Attempt to find product by ID or name
        product = None
        if product_input.isdigit():
            product = next((p for p in products if p['id'] == int(product_input)), None)
        else:
            product = next((p for p in products if p['name'].lower() == product_input), None)

        # If product doesn't exist, guide user to create a new one
        if not product:
            print("Creating new product")
            new_id = max(p['id'] for p in products) + 1 if products else 1  # Generate unique ID

            # Get new product details with validations
            while True:
                name = ' '.join(input("Product Name: ").split())
                if name:
                    break
                print("Product name cannot be empty")

            brand = ' '.join(input("Brand: ").split()) or "Generic"
            price = get_positive_number("Price per unit: Rs.", is_float=True)
            origin = ' '.join(input("Origin: ").split()) or "Unknown"

            # Initialize new product with 0 quantity (will add stock below)
            product = {
                'id': new_id,
                'name': name,
                'brand': brand,
                'quantity': 0,
                'price': price,
                'origin': origin
            }
            products.append(product)

            print(f"New product created: {product['name']} (ID: {product['id']})")

        # Input quantity to be added to stock
        add_qty = get_positive_number(f"\nCurrent stock: {product['quantity']}\nQuantity to add: ")
        original_price = product['price']

        # Update stock quantity
        product['quantity'] += add_qty

        # Optional: allow vendor to update the product's price
        try:
            new_price = input(f"New price (current: Rs.{original_price:.2f}, press Enter to keep): ")
            if new_price:
                product['price'] = float(new_price)
                # Validate that new price is a positive number
                if product['price'] <= 0:
                    print("Price reset to previous value - must be positive")
                    product['price'] = original_price
        except ValueError:
            print("Invalid price format. Keeping previous value")

        # Persist the updated product list to storage
        save_products(products)

        # Create a restock invoice
        invoice = generate_invoice(vendor, [{
            'name': product['name'],
            'qty': add_qty,
            'free': 0,  # No free units for restocking
            'total': add_qty * product['price']
        }], add_qty * product['price'], "restock")

        print("\n" + " Restock Complete ".center(40, '═'))
        print(f"Restock invoice: {invoice}")
        print(f"New stock for {product['name']}: {product['quantity']} units")

    except Exception as e:
        # Handle unexpected errors (e.g., file issues, input exceptions)
        print(f"Restock error: {e}")
