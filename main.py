import tkinter as tk
from tkinter import ttk
import json

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            "type": "Product",
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

    @staticmethod
    def from_dict(data):
        if data["type"] == "Perishable":
            return PerishableProduct(
                data["product_id"],
                data["name"],
                data["price"],
                data["quantity"],
                data.get("expiry_date", ""),
                data.get("storage_temp", "")
            )
        elif data["type"] == "Electronic":
            return ElectronicProduct(
                data["product_id"],
                data["name"],
                data["price"],
                data["quantity"],
                data.get("warranty_period", ""),
                data.get("power_usage", "")
            )
        else:
            return Product(
                data["product_id"],
                data["name"],
                data["price"],
                data["quantity"]
            )


class PerishableProduct(Product):
    def __init__(self, product_id, name, price, quantity, expiry_date, storage_temp):
        super().__init__(product_id, name, price, quantity)
        self.expiry_date = expiry_date
        self.storage_temp = storage_temp

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Perishable"
        data["expiry_date"] = self.expiry_date
        data["storage_temp"] = self.storage_temp
        return data
    

class ElectronicProduct(Product):
    def __init__(self, product_id, name, price, quantity, warranty_period, power_usage):
        super().__init__(product_id, name, price, quantity)
        self.warranty_period = warranty_period
        self.power_usage = power_usage

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Electronic"
        data["warranty_period"] = self.warranty_period
        data["power_usage"] = self.power_usage
        return data

class Inventory:
    def __init__(self):
        self.products = []

    def load_data(self, file="inventory.json"):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                self.products = [Product.from_dict(p) for p in data]
        except:
            self.products = []

    def save_data(self, file="inventory.json"):
        with open(file, "w") as f:
            json.dump([p.to_dict() for p in self.products], f, indent=4)

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, pid):
        self.products = [p for p in self.products if p.product_id != pid]

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width / 2 - width / 2)
    center_y = int(screen_height / 2 - height / 2)

    root.geometry(f"{width}x{height}+{center_x}+{center_y}")

root = tk.Tk()
root.title("SmartStock")
center_window(root, 900, 500)

top_frame = tk.Frame(root, bg="white", height=50)
top_frame.pack(side="top", fill="x")
tk.Label(top_frame, text="Total: 0").pack(side="left", padx=20)
tk.Label(top_frame, text="Low Stock: 0").pack(side="left", padx=20)
tk.Label(top_frame, text="Expiring stock: ".pack(side="left", padx=20))
tk.Label(top_frame, text="Value: £0").pack(side="left", padx=20)

menu_frame = tk.Frame(root, bg="lightgrey", width=150)
menu_frame.pack(side="left", fill="y")
menu_frame.pack_propagate(False)  
tk.Button(menu_frame, text="Dashboard").pack(fill="x", pady=5)
tk.Button(menu_frame, text="Edit product").pack(fill="x", pady=5)
tk.Button(menu_frame, text="search").pack(fill="x", pady=5)
tk.Button(menu_frame, text="Alerts").pack(fill="x", pady=5)

content_frame = tk.Frame(root)
content_frame.pack(side="right", expand=True, fill="both")
cards_frame = tk.Frame(content_frame)
cards_frame.pack(expand=True, fill="both")

cards_frame.grid_rowconfigure((0,1), weight=1)
cards_frame.grid_columnconfigure((0,1), weight=1)

def create_card(parent, title, value):
    frame = tk.Frame(parent, bg="white", bd=2, relief="ridge")

    tk.Label(frame, text=title).pack(expand=True)
    tk.Label(frame, text=value, font=("Arial", 18, "bold")).pack(expand=True)

    return frame

card1 = create_card(cards_frame, "Total Items", "0")
card2 = create_card(cards_frame, "Low Stock", "0")
card3 = create_card(cards_frame, "Total Value", "£0")
card4 = create_card(cards_frame, "Expiring Soon", "0")

card1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
card2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
card3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
card4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

root.mainloop()
