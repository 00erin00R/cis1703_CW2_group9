def view_details(self):
    try:
        selected_index = self.listbox.curselection()[0]
        product = self.app.inventory.products[selected_index]

        details = f"""
        ID: {product.product_id}
        Name: {product.name}
        Price: £{product.price}
        Quantity: {product.quantity}
        """

        if isinstance(product, PerishableProduct):
            details += f"\nExpiry Date: {product.expiry_date}\nStorage Temp: {product.storage_temp}"

        elif isinstance(product, ElectronicProduct):
            details += f"\nWarranty: {product.warranty_period}\nPower Usage: {product.power_usage}"

        messagebox.showinfo("Product Details", details)

    except:
        messagebox.showerror("Error", "Please select an item")