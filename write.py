import datetime  # Used to generate timestamped filenames

# Save the list of product dictionaries to a text file
def save_products(products):
    try:
        with open('product.txt', 'w') as file:  # Open in write mode (overwrite)
            for p in products:
                # Write each product as a comma-separated line
                file.write(f"{p['id']},{p['name']},{p['brand']},{p['quantity']},{p['price']},{p['origin']}\n")
    except Exception as e:
        print(f" Error saving products: {e}")  # Handle file writing error

# Generate and save a transaction invoice (for sale or restock)
def generate_invoice(customer_name, items, total, transaction_type):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Unique timestamp
    filename = f"{transaction_type}_invoice_{timestamp}.txt"  # File name based on type and time
    try:
        with open(filename, 'w') as f:
            # Header section
            f.write("=" * 50 + "\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Customer: {customer_name}\n")
            f.write("Items:\n")
            # List each item and handle free items
            for item in items:
                if item['free'] > 0:
                    f.write(f"- {item['name']}: {item['qty']} (+{item['free']} free) = Rs.{item['total']:.2f}\n")
                else:
                    f.write(f"- {item['name']}: {item['qty']} = Rs.{item['total']:.2f}\n")
            # Total and footer
            f.write(f"Total: Rs.{total:.2f}\n")
            f.write("=" * 50 + "\n")
        return filename  # Return the name of the generated file
    except Exception as e:
        print(f" Error generating invoice: {e}")  # Log error if writing fails
        return None
