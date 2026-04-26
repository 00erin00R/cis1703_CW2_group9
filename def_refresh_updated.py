def refresh(self):
    self.listbox.delete(0, tk.END)

    for p in self.app.inventory.products:
        text = f"ID: {p.product_id} | {p.name} | £{p.price} | Qty: {p.quantity}"

        if isinstance(p, PerishableProduct):
            text += f" | Exp: {p.expiry_date}"

        elif isinstance(p, ElectronicProduct):
            text += f" | Warranty: {p.warranty_period}"

        self.listbox.insert(tk.END, text)