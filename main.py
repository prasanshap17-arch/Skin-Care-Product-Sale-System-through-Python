# Import functions from other modules
from read import display_products
from operations import process_sale, process_restock

# Main menu function to control the application
def main_menu():
    while True:
        print("\n" + " WeCare Skin Care System ".center(50, '═'))  # Centered title
        print("1. Display Products")
        print("2. Process Sale")
        print("3. Restock")
        print("4. Exit")
        print("═" * 50)  # Decorative line

        choice = input("Please choose an option (1-4): ").strip()  # Get and clean input

        # Call appropriate function based on user input
        if choice == '1':
            display_products()
        elif choice == '2':
            process_sale()
        elif choice == '3':
            process_restock()
        elif choice == '4':
            print("\n" + " Thank you for using WeCare! ".center(50, '═'))  # Goodbye message
            break
        else:
            print("Invalid choice. Please select 1-4")  # Invalid input handler

# Run the menu only if this file is executed directly
if __name__ == "__main__":
    main_menu()
