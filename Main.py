import json
import datetime
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
        except FileNotFoundError:
            # create empty file if it doesn't exist
            with open(file, "w") as f:
                json.dump([], f)
            self.products = []
        except Exception as e:
            print("Error loading JSON:", e)
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

        for F in (Dashboard, AddRemovePage, Update, Search, ViewData, Alert):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        tk.Button(self.sidebar, text="Dashboard",
                  command=lambda: self.show_frame(Dashboard)).pack(fill="x")

        tk.Button(self.sidebar, text="Add / Remove",
                  command=lambda: self.show_frame(AddRemovePage)).pack(fill="x")
        
        tk.Button(self.sidebar, text="Update",
                  command=lambda: self.show_frame(Update)).pack(fill="x")
        
        tk.Button(self.sidebar, text="Search",
                  command=lambda: self.show_frame(Search)).pack(fill="x")
        
        tk.Button(self.sidebar, text="View data",
                  command=lambda: self.show_frame(ViewData)).pack(fill="x")

        tk.Button(self.sidebar, text="Alert",
                  command=lambda: self.show_frame(Alert)).pack(fill="x")

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

        self.info = tk.Label(self, text="")

        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x")
        tk.Label(top_frame, text="Total: 0").pack(side="left", padx=20)
        tk.Label(top_frame, text="Low Stock: 0").pack(side="left", padx=20)
        tk.Label(top_frame, text="Expiring stock: ").pack(side="left", padx=20)
        tk.Label(top_frame, text="Value: £0").pack(side="left", padx=20)

        menu_frame = tk.Frame(self)
        menu_frame.pack(side="left", fill="y")
        menu_frame.pack_propagate(False)  
        tk.Button(menu_frame, text="Dashboard").pack(fill="x", pady=5)
        tk.Button(menu_frame, text="Edit product").pack(fill="x", pady=5)
        tk.Button(menu_frame, text="search").pack(fill="x", pady=5)
        tk.Button(menu_frame, text="Alerts").pack(fill="x", pady=5)

        content_frame = tk.Frame(self)
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

class Update(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Update Product", font=("Arial", 16)).pack(pady=10)

        # List of products
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self, text="Edit Selected", command=self.update_product).pack(pady=5)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for p in self.app.inventory.products:
            self.listbox.insert(tk.END, f"{p.product_id} - {p.name}")

    def update_product(self):
        try:
            selected_index = self.listbox.curselection()[0]
            product = self.app.inventory.products[selected_index]

            update_window = tk.Toplevel(self)
            update_window.title("Update Product")
            update_window.geometry("300x250")

            tk.Label(update_window, text="Name").pack()
            name_entry = tk.Entry(update_window)
            name_entry.insert(0, product.name)
            name_entry.pack()

            tk.Label(update_window, text="Price").pack()
            price_entry = tk.Entry(update_window)
            price_entry.insert(0, str(product.price))
            price_entry.pack()

            tk.Label(update_window, text="Quantity").pack()
            quantity_entry = tk.Entry(update_window)
            quantity_entry.insert(0, str(product.quantity))
            quantity_entry.pack()

            def save_update():
                try:
                    product.name = name_entry.get()
                    product.price = float(price_entry.get())
                    product.quantity = int(quantity_entry.get())

                    self.app.inventory.save_data()
                    self.refresh()

                    messagebox.showinfo("Success", "Product Updated")
                    update_window.destroy()

                except:
                    messagebox.showerror("Error", "Invalid Input")

            tk.Button(update_window, text="Save", command=save_update).pack(pady=10)

        except IndexError:
            messagebox.showerror("Error", "Please select an item")

class Search(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Search Products", font=("Arial", 16)).pack(pady=10)

            # Search input
        self.search_entry = tk.Entry(self)
        self.search_entry.pack(pady=5)

        tk.Button(self, text="Search", command=self.perform_search).pack(pady=5)

        # Results list
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh(self):
        self.listbox.delete(0, tk.END)

    def perform_search(self):
        query = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)

        for p in self.app.inventory.products:
            # Search by ID or Name
            if query in p.product_id.lower() or query in p.name.lower():
                self.listbox.insert(
                    tk.END,
                    f"{p.product_id} - {p.name} (£{p.price}, Qty: {p.quantity})"
                )

        if self.listbox.size() == 0:
            self.listbox.insert(tk.END, "No results found")    

class ViewData(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Inventory Data", font=("Arial", 16)).pack(pady=10)

        # Table
        columns = ("ID", "Name", "Price", "Quantity", "Type")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=60, anchor="center", stretch=False)

        self.tree.heading("Name", text="Name")
        self.tree.column("Name", width=180, anchor="center")

        self.tree.heading("Price", text="Price")
        self.tree.column("Price", width=80, anchor="center")

        self.tree.heading("Quantity", text="Quantity")
        self.tree.column("Quantity", width=80, anchor="center")

        self.tree.heading("Type", text="Type")
        self.tree.column("Type", width=100, anchor="center")

    def refresh(self):
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert updated data
        for p in self.app.inventory.products:
            ptype = "Product"
            extra = ""

            if isinstance(p, PerishableProduct):
                ptype = "Perishable"
                extra = f"Expiry: {p.expiry_date}, Temp: {p.storage_temp}"

            elif isinstance(p, ElectronicProduct):
                ptype = "Electronic"
                extra = f"Warranty: {p.warranty_period}, Power: {p.power_usage}"

            self.tree.insert("", "end", values=(
                p.product_id,
                p.name,
                f"£{p.price:.2f}",
                p.quantity,
                ptype,
                extra
            ))

class Alert(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Alerts", font=("Arial", 16)).pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Refresh Alerts", command=self.refresh).pack()

        # Alert list
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh(self):
        self.listbox.delete(0, tk.END)

        today = datetime.date.today()
        low_stock_threshold = 5  # you can change this

        for p in self.app.inventory.products:

            # LOW STOCK ALERT
            if p.quantity <= low_stock_threshold:
                self.listbox.insert(
                    tk.END,
                    f" LOW STOCK: {p.name} (Qty: {p.quantity})"
                )

            # EXPIRY ALERT (only for Perishable)
            if isinstance(p, PerishableProduct) and p.expiry_date:
                try:
                    expiry = datetime.datetime.strptime(p.expiry_date, "%Y-%m-%d").date()
                    days_left = (expiry - today).days

                    if days_left <= 3:
                        self.listbox.insert(
                            tk.END,
                            f" EXPIRING SOON: {p.name} (in {days_left} days)"
                        )

                except:
                    self.listbox.insert(
                        tk.END,
                        f" Invalid expiry date for {p.name}"
                    )

        # If no alerts
        if self.listbox.size() == 0:
            self.listbox.insert(tk.END, "No alerts ")

# start page

if __name__ == "__main__":
    app = App()
    app.mainloop()
