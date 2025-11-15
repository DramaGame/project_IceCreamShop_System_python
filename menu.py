from file_manager import FileManager
from typing import List, Dict

class MenuItem:
    def __init__(self, item_id: str, name: str, price: float, category: str):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.category = category  # flavor, topping, container
    
    def to_dict(self) -> Dict:
        return {
            'item_id': self.item_id,
            'name': self.name,
            'price': self.price,
            'category': self.category
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MenuItem':
        return cls(
            item_id=data['item_id'],
            name=data['name'],
            price=data['price'],
            category=data['category']
        )
    
    def __str__(self) -> str:
        return f"{self.name} - {self.price:.2f}"

class MenuManager:
    def __init__(self):
        self.file_manager = FileManager()
        self.menu_items: List[MenuItem] = []
        self.load_menu()
    
    def load_menu(self):
        """Load menu from file"""
        menu_data = self.file_manager.load_from_file("menu.json")
        self.menu_items = [MenuItem.from_dict(item) for item in menu_data]
    
    def save_menu(self):
        """Save menu to file"""
        menu_data = [item.to_dict() for item in self.menu_items]
        return self.file_manager.save_to_file("menu.json", menu_data)
    
    def add_menu_item(self, item_id: str, name: str, price: float, category: str) -> bool:
        """Add new item to menu"""
        new_item = MenuItem(item_id, name, price, category)
        self.menu_items.append(new_item)
        return self.save_menu()
    
    def get_items_by_category(self, category: str) -> List[MenuItem]:
        """Get all items of specific category"""
        return [item for item in self.menu_items if item.category == category]
    
    def get_item_by_id(self, item_id: str) -> MenuItem:
        """Get menu item by ID"""
        for item in self.menu_items:
            if item.item_id == item_id:
                return item
        return None
    
    def display_menu(self):
        """Display complete menu"""
        print("\n" + "="*50)
        print("           ICE CREAM SHOP MENU")
        print("="*50)
        
        categories = {'flavor': 'FLAVORS', 'topping': 'TOPPINGS', 'container': 'CONTAINERS'}
        
        for category, title in categories.items():
            print(f"\n{title}:")
            items = self.get_items_by_category(category)
            for item in items:
                print(f"  {item.item_id}. {item}")