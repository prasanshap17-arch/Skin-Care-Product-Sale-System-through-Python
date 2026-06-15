# Load products from file and return them as a list of dictionaries
def load_products():
    try:
        products = []
        with open('product.txt', 'r') as file:  # Open product file for reading
            for line in file:
                line = line.rstrip('\n')  # Remove newline at end
                if not line:
                    continue  # Skip blank lines
                parts = line.split(',')
                if len(parts) != 6:
                    continue  # Skip malformed lines
                product_id, name, brand, quantity, price, origin = parts
                try:
                    # Convert values and build product dictionary
                    product = {
                        'id': int(product_id),
                        'name': ' '.join(name.split()),  # Normalize whitespace
                        'brand': ' '.join(brand.split()),
                        'quantity': int(quantity),
                        'price': float(price),
                        'origin': ' '.join(origin.split())
                    }
                    products.append(product)
                except ValueError:
                    continue  # Skip entries with invalid data types
        return products
    except FileNotFoundError:
        print("No product file found. Starting fresh.")
        return []  # Start with an empty list if file doesn’t exist
    except Exception as e:
        print(f" Error loading products: {e}")
        return []  # Fail-safe for unknown errors

# Display all available products in tabular format
def display_products():
    products = load_products()
    print("\n" + " Available Products ".center(90, '═'))  # Header
    print("{:<8} {:<20} {:<15} {:<10} {:<15} {:<15}".format(
        "ID", "Product", "Brand", "Quantity", "Price", "Origin"))  # Column titles
    print("═" * 90)
    for p in products:
        print("{:<8} {:<20} {:<15} {:<10} {:<15.2f} {:<15}".format(
            p['id'], p['name'], p['brand'], p['quantity'], p['price'], p['origin']))  # Product row
    print("═" * 90 + "\n")
