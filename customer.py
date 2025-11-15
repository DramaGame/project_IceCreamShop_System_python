from file_manager import FileManager
from typing import List, Dict

class Customer:
    def __init__(self, customer_id: str, name: str):
        self.customer_id = customer_id
        self.name = name
        self.order_history: List[str] = []  # List of order IDs
    
    def to_dict(self) -> Dict:
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'order_history': self.order_history
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Customer':
        customer = cls(
            customer_id=data['customer_id'],
            name=data['name']
        )
        customer.order_history = data.get('order_history', [])
        return customer
    
    def add_order_to_history(self, order_id: str):
        """Add order to customer's history"""
        self.order_history.append(order_id)

class CustomerManager:
    def __init__(self):
        self.file_manager = FileManager()
        self.customers: List[Customer] = []
        self.load_customers()
    
    def load_customers(self):
        """Load customers from file"""
        customers_data = self.file_manager.load_from_file("customers.json")
        self.customers = [Customer.from_dict(customer) for customer in customers_data]
    
    def save_customers(self):
        """Save customers to file"""
        customers_data = [customer.to_dict() for customer in self.customers]
        return self.file_manager.save_to_file("customers.json", customers_data)
    
    def add_customer(self, customer_id: str, name: str) -> Customer:
        """Add new customer"""
        customer = Customer(customer_id, name)
        self.customers.append(customer)
        self.save_customers()
        return customer
    
    def find_customer_by_id(self, customer_id: str) -> Customer:
        """Find customer by ID"""
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None
    
    def update_customer_order_history(self, customer_id: str, order_id: str):
        """Update customer's order history"""
        customer = self.find_customer_by_id(customer_id)
        if customer:
            customer.add_order_to_history(order_id)
            self.save_customers()