from menu import MenuManager
from customer import CustomerManager
from order import OrderManager

class IceCreamShopSystem:
    def __init__(self):
        self.menu_manager = MenuManager()
        self.customer_manager = CustomerManager()
        self.order_manager = OrderManager(self.menu_manager, self.customer_manager)
        self.initialize_sample_data()
    
    def initialize_sample_data(self):
        """Initialize with sample data if empty"""
        if not self.menu_manager.menu_items:
            # Add sample menu items
            sample_items = [
                ('F01', 'Vanilla', 200, 'flavor'),
                ('F02', 'Chocolate', 200, 'flavor'),
                ('F03', 'Strawberry', 300, 'flavor'),
                ('T01', 'Sprinkles', 60, 'topping'),
                ('T02', 'Hot Fudge', 75, 'topping'),
                ('C01', 'Regular Cone', 100, 'container'),
                ('C02', 'Waffle Cone', 200, 'container'),
                ('C03', 'Cup', 50, 'container')
            ]
            
            for item_id, name, price, category in sample_items:
                self.menu_manager.add_menu_item(item_id, name, price, category)
    
    def display_main_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("       ICE CREAM SHOP MANAGEMENT SYSTEM")
        print("="*50)
        print("1. View Menu")
        print("2. Place New Order")
        print("3. View All Orders")
        print("4. Customer Management")
        print("5. Exit")
    
    def place_new_order(self):
        """Handle new order placement"""
        print("\n--- Place New Order ---")
        
        # Get customer information
        customer_name = input("Enter customer name: ")
        customer_id = input("Enter customer ID: ")
        
        # Check if customer exists, if not create new
        customer = self.customer_manager.find_customer_by_id(customer_id)
        if not customer:
           
            customer = self.customer_manager.add_customer(customer_id, customer_name)
            print(f"New customer created: {customer_name}")
        
        # Create new order
        order = self.order_manager.create_order(customer_id)
        
        # Add items to order
        self.menu_manager.display_menu()
        
        while True:
            print("\nAdd items to order (enter 'done' to finish):")
            item_id = input("Enter item ID: ")
            
            if item_id.lower() == 'done':
                break
            
            menu_item = self.menu_manager.get_item_by_id(item_id)
            if menu_item:
                quantity = int(input(f"Enter quantity for {menu_item.name}: "))
                order.add_item(item_id, quantity)
                print(f"Added {menu_item.name} x{quantity}")
            else:
                print("Invalid item ID!")
        
        # Place order
        if order.items:
            self.order_manager.place_order(order)
            print(f"\nOrder placed successfully!")
            print(f"Order ID: {order.order_id}")
            print(f"Total Amount: {order.total_amount:.2f}")
        else:
            print("No items in order. Order cancelled.")
    
    def view_all_orders(self):
        """Display all orders"""
        print("\n--- All Orders ---")
        if not self.order_manager.orders:
            print("No orders found.")
            return
        
        for order in self.order_manager.orders:
            print(order)
        
        # Option to view details
        view_details = input("\nView order details? (enter order ID or 'no'): ")
        if view_details.lower() != 'no':
            self.order_manager.display_order_details(view_details)
    
    def customer_management(self):
        """Handle customer management"""
        print("\n--- Customer Management ---")
        print("1. View All Customers")
        print("2. Add New Customer")
        choice = input("Enter choice: ")
        
        if choice == '1':
            print("\n--- All Customers ---")
            for customer in self.customer_manager.customers:
                print(f"ID: {customer.customer_id}, Name: {customer.name}")
        
        elif choice == '2':
            customer_id = input("Enter customer ID: ")
            name = input("Enter customer name: ")
        
            
            self.customer_manager.add_customer(customer_id, name)
            print("Customer added successfully!")
    
    def run(self):
        """Main application loop"""
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                self.menu_manager.display_menu()
            elif choice == '2':
                self.place_new_order()
            elif choice == '3':
                self.view_all_orders()
            elif choice == '4':
                self.customer_management()
            elif choice == '5':
                print("Thank you for using Ice Cream Shop System!")
                break
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    system = IceCreamShopSystem()
    system.run()