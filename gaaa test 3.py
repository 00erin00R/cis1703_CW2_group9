import json
import tkinter as tk
from tkinter import ttk, messagebox

#the Classes for the products to be strucutred and should be reused in any test peices or seperate files as all feature need to interact with this class

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


# to manage the inventory 

class Inventory:
    def __init__(self):
        self.products = []

    def load_data(self, file="data.json"):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                self.products = [Product.from_dict(p) for p in data]
        except:
            self.products = []

    def save_data(self, file="data.json"):
        with open(file, "w") as f:
            json.dump([p.to_dict() for p in self.products], f, indent=4)

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, pid):
        self.products = [p for p in self.products if p.product_id != pid]


# for basic page structure 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory System")
        self.geometry("800x500")

        self.inventory = Inventory()
        self.inventory.load_data()

        self.sidebar = tk.Frame(self, bg="lightgrey", width=150)
        self.sidebar.pack(side="left", fill="y")

        self.container = tk.Frame(self)
        self.container.pack(side="right", expand=True, fill="both")

        self.frames = {}

        for F in (Dashboard, AddRemovePage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        tk.Button(self.sidebar, text="Dashboard",
                  command=lambda: self.show_frame(Dashboard)).pack(fill="x")

        tk.Button(self.sidebar, text="Add / Remove",
                  command=lambda: self.show_frame(AddRemovePage)).pack(fill="x")

        self.show_frame(Dashboard)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.refresh()
        frame.tkraise()


#dashboard page for test 

class Dashboard(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Dashboard", font=("Arial", 18)).pack(pady=20)

        self.info = tk.Label(self, text="")
        self.info.pack()

    def refresh(self):
        total = len(self.app.inventory.products)
        self.info.config(text=f"Total Items: {total}")


class AddRemovePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        left = tk.Frame(self)
        left.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        right = tk.Frame(self)
        right.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # ADD
        tk.Label(left, text="Add Item", font=("Arial", 14)).pack(pady=5)

        tk.Label(left, text="Product ID").pack()
        self.id_entry = tk.Entry(left)
        self.id_entry.pack()

        tk.Label(left, text="Name").pack()
        self.name_entry = tk.Entry(left)
        self.name_entry.pack()

        tk.Label(left, text="Price").pack()
        self.price_entry = tk.Entry(left)
        self.price_entry.pack()

        tk.Label(left, text="Quantity").pack()
        self.qty_entry = tk.Entry(left)
        self.qty_entry.pack()

        tk.Label(left, text="Product Type (optional)").pack()
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(
            left,
            textvariable=self.type_var,
            values=["", "Perishable", "Electronic"]
        )
        self.type_dropdown.pack()

        self.extra_frame = tk.Frame(left)
        self.extra_frame.pack()

        self.type_dropdown.bind("<<ComboboxSelected>>", self.update_fields)

        tk.Button(left, text="Add", command=self.add_item).pack(pady=5)

        # REMOVE
        tk.Label(right, text="Remove Item", font=("Arial", 14)).pack(pady=5)

        tk.Label(right, text="Product ID").pack()
        self.remove_entry = tk.Entry(right)
        self.remove_entry.pack()

        tk.Button(right, text="Remove", command=self.remove_item).pack(pady=5)

        # LIST
        self.listbox = tk.Listbox(self)
        self.listbox.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

    def update_fields(self, event=None):
        for widget in self.extra_frame.winfo_children():
            widget.destroy()

        selected = self.type_var.get()

        if selected == "Perishable":
            tk.Label(self.extra_frame, text="Expiry Date (YYYY-MM-DD)").pack()
            self.expiry_entry = tk.Entry(self.extra_frame)
            self.expiry_entry.pack()

            tk.Label(self.extra_frame, text="Storage Temp").pack()
            self.temp_entry = tk.Entry(self.extra_frame)
            self.temp_entry.pack()

        elif selected == "Electronic":
            tk.Label(self.extra_frame, text="Warranty Period").pack()
            self.warranty_entry = tk.Entry(self.extra_frame)
            self.warranty_entry.pack()

            tk.Label(self.extra_frame, text="Power Usage").pack()
            self.power_entry = tk.Entry(self.extra_frame)
            self.power_entry.pack()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for p in self.app.inventory.products:
            self.listbox.insert(tk.END, f"{p.product_id} - {p.name}")

    def add_item(self):
        try:
            pid = self.id_entry.get()
            name = self.name_entry.get()
            price = float(self.price_entry.get())
            qty = int(self.qty_entry.get())
            ptype = self.type_var.get()

            if ptype == "Perishable":
                p = PerishableProduct(
                    pid, name, price, qty,
                    self.expiry_entry.get(),
                    self.temp_entry.get()
                )

            elif ptype == "Electronic":
                p = ElectronicProduct(
                    pid, name, price, qty,
                    self.warranty_entry.get(),
                    self.power_entry.get()
                )

            else:
                p = Product(pid, name, price, qty)

            self.app.inventory.add_product(p)
            self.app.inventory.save_data()

            messagebox.showinfo("Success", "Item Added")
            self.refresh()

        except:
            messagebox.showerror("Error", "Invalid input")

    def remove_item(self):
        pid = self.remove_entry.get()
        self.app.inventory.remove_product(pid)
        self.app.inventory.save_data()

        messagebox.showinfo("Removed", "Item Removed")
        self.refresh()


# start page

if __name__ == "__main__":
    app = App()
    app.mainloop()