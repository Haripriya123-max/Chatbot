# Shopping cart with bill generation
# User Details
name = "Rohith"
address = "good place"
phone_number = "9791523873"

# Item list with price
items = [
    {"name": "Banana", "price": 6},
    {"name": "Mango", "price": 5},
    {"name": "Kiwi", "price": 4},
    {"name": "Berry", "price": 7},
    {"name": "Apple", "price": 8},
    {"name": "Cherry", "price": 9}
]

# Cart dictionary to store item_name: quantity
cart = {}

def display_menu():
    print(f"\nName: {name}")
    print(f"Address: {address}")
    print(f"Phone Number: {phone_number}")
    print("\n----------- Items Menu -----------")
    print("Sno  Item Name      Price each(in $)")
    print("------------------------------------")
    for i, item in enumerate(items, start=1):
        print(f"{i}    {item['name']:<12} {item['price']:.2f}")
    print("7    Exit")
    print("------------------------------------")

def update_cart(choice, quantity):
    item = items[choice - 1]
    item_name = item['name']
    if item_name in cart:
        cart[item_name] += quantity
    else:
        cart[item_name] = quantity
    print("Cart Updated...\n")

def generate_bill():
    print("\n----------- FINAL BILL -----------")
    print(f"Customer Name: {name}")
    print(f"Address      : {address}")
    print(f"Phone Number : {phone_number}")
    print("----------------------------------")
    print(f"{'Item':<12} {'Qty':<5} {'Price($)':<10} {'Total($)':<10}")
    print("----------------------------------")
    grand_total = 0
    for item_name in cart:
        quantity = cart[item_name]
        price = next(i['price'] for i in items if i['name'] == item_name)
        total = quantity * price
        grand_total += total
        print(f"{item_name:<12} {quantity:<5} {price:<10.2f} {total:<10.2f}")
        print("----------------------------------")
    print(f"{'Grand Total':<29} {grand_total:.2f}")
    print("----------------------------------")
    print("Thank you for shopping with us!")

# Main loop
while True:
    display_menu()
    try:
        choice = int(input("Your Choice: "))
        if choice == 7:
            break
        elif 1 <= choice <= 6:
            quantity = int(input("Input Quantity: "))
            if quantity <= 0:
                print("Quantity must be a positive integer.\n")
                continue
            update_cart(choice, quantity)
        else:
            print("Invalid choice. Try again.\n")
    except ValueError:
        print("Invalid input. Enter numbers only.\n")

# Generate the bill
if cart:
    generate_bill()
else:
    print("No items purchased.")