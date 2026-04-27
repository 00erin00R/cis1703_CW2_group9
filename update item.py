def update_product(self):
    try:
        selected_index = self.listbox.curselection()[0]
        product = self.app.inventory.products[selected_index]

        update_window = tk.Toplevel(self.root)
        update_window.title("Update Product")
        update_window.geometry("300x250")

        tk.Label(update_window, text="Name").pack()
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, product.name)
        name_entry.pack()

        tk.Label(update_window, text="Price").pack()
        price_entry = tk.Entry(update_window)
        price_entry.insert(0, product.price)
        price_entry.pack()

        tk.Label(update_window, text="Quantity").pack()
        quantity_entry = tk.Entry(update_window)
        quantity_entry.insert(0, product.quantity)
        quantity_entry.pack()

        def save_update():
            try:
                product.name = name_entry.get()
                product.price = float(price_entry.get())
                product.quantity = int(quantity_entry.get())

                self.refresh()
                self.app.inventory.save_products()

                messagebox.showinfo("Product Updated")
                update_window.destroy()

            except:
                messagebox.showerror("Invalid Input")

        tk.Button(update_window, text="Save", command=save_update).pack(pady=10)

    except:
        messagebox.showerror("Please select an item")
