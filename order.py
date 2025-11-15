from file_manager import FileManager
from datetime import datetime
from typing import List, Dict
import random

class OrderItem:
    def __init__(self, item_id: str, quantity: int = 1):
        self.item_id = item_id
        self.quantity = quantity
    
    def to_dict(self) -> Dict:
        return {
            'item_id': self.item_id,
            'quantity': self.quantity
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'OrderItem':
        return cls(
            item_id=data['item_id'],
            quantity=data.get('quantity', 1)
        )

class Order:
    def __init__(self, order_id: str, customer_id: str):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.items: List[OrderItem] = []
        self.status = "pending"  # pending, preparing, ready, completed
        self.total_amount = 0.0
    
    def to_dict(self) -> Dict:
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'order_date': self.order_date,
            'items': [item.to_dict() for item in self.items],
            'status': self.status,
            'total_amount': self.total_amount
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Order':
        order = cls(
            order_id=data['order_id'],
            customer_id=data['customer_id']
        )
        order.order_date = data['order_date']
        order.items = [OrderItem.from_dict(item) for item in data['items']]
        order.status = data['status']
        order.total_amount = data['total_amount']
        return order
    
    def add_item(self, item_id: str, quantity: int = 1):
        """Add item to order"""
        self.items.append(OrderItem(item_id, quantity))
    
    def calculate_total(self, menu_manager) -> float:
        """Calculate total amount using menu prices"""
        total = 0.0
        for order_item in self.items:
            menu_item = menu_manager.get_item_by_id(order_item.item_id)
            if menu_item:
                total += menu_item.price * order_item.quantity
        self.total_amount = total
        return total
    
    def __str__(self) -> str:
        return f"Order #{self.order_id} - Customer: {self.customer_id} - Total: {self.total_amount:.2f}"

class OrderManager:
    def __init__(self, menu_manager, customer_manager):
        self.file_manager = FileManager()
        self.menu_manager = menu_manager
        self.customer_manager = customer_manager
        self.orders: List[Order] = []
        self.load_orders()
    
    def load_orders(self):
        """Load orders from file"""
        orders_data = self.file_manager.load_from_file("orders.json")
        self.orders = [Order.from_dict(order) for order in orders_data]
    
    def save_orders(self):
        """Save orders to file"""
        orders_data = [order.to_dict() for order in self.orders]
        return self.file_manager.save_to_file("orders.json", orders_data)
    
    def generate_order_id(self) -> str:
        """Generate unique order ID"""
        return f"ORD{random.randint(1000, 9999)}"
    
    def create_order(self, customer_id: str) -> Order:
        """Create new order"""
        order_id = self.generate_order_id()
        order = Order(order_id, customer_id)
        self.orders.append(order)
        return order
    
    def place_order(self, order: Order) -> bool:
        """Finalize and save order"""
        # Calculate total
        order.calculate_total(self.menu_manager)
        
        # Update customer history
        self.customer_manager.update_customer_order_history(
            order.customer_id, order.order_id
        )
        
        # Save to file
        return self.save_orders()
    
    def get_order_by_id(self, order_id: str) -> Order:
        """Get order by ID"""
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None
    
    def update_order_status(self, order_id: str, new_status: str) -> bool:
        """Update order status"""
        order = self.get_order_by_id(order_id)
        if order:
            order.status = new_status
            return self.save_orders()
        return False
    
    def display_order_details(self, order_id: str):
        """Display detailed order information"""
        order = self.get_order_by_id(order_id)
        if not order:
            print("Order not found!")
            return
        
        customer = self.customer_manager.find_customer_by_id(order.customer_id)
        
        print(f"\nOrder #: {order.order_id}")
        print(f"Customer: {customer.name if customer else 'Unknown'}")
        print(f"Date: {order.order_date}")
        print(f"Status: {order.status}")
        print(f"Total: ${order.total_amount:.2f}")
        print("\nItems:")
        for order_item in order.items:
            menu_item = self.menu_manager.get_item_by_id(order_item.item_id)
            if menu_item:
                print(f"  - {menu_item.name} x{order_item.quantity} - {menu_item.price * order_item.quantity:.2f}")