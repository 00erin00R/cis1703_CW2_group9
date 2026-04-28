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

        def create_card(parent, title):
            frame = tk.Frame(parent, bg="white", bd=2, relief="ridge")

            tk.Label(frame, text=title).pack(expand=True)
            value_label = tk.Label(frame, text="0", font=("Arial", 18, "bold"))
            value_label.pack(expand=True)

            return frame, value_label


        self.card1, self.total_label = create_card(cards_frame, "Total Items")
        self.card2, self.low_stock_label = create_card(cards_frame, "Low Stock")
        self.card3, self.value_label = create_card(cards_frame, "Total Value")
        self.card4, self.expiry_label = create_card(cards_frame, "Expiring Soon")


        self.card1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.card2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.card3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.card4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    def refresh(self):
        products = self.app.inventory.products

        total_items = len(products)

        low_stock_threshold = 5
        low_stock = sum(1 for p in products if p.quantity <= low_stock_threshold)

        total_value = sum(p.price * p.quantity for p in products)

        today = datetime.date.today()
        expiring_soon = 0

        for p in products:
            if isinstance(p, PerishableProduct) and p.expiry_date:
                try:
                    expiry = datetime.datetime.strptime(p.expiry_date, "%Y-%m-%d").date()
                    days_left = (expiry - today).days

                    if days_left <= 3:
                        expiring_soon += 1
                except:
                    pass

        # Update UI
        self.total_label.config(text=str(total_items))
        self.low_stock_label.config(text=str(low_stock))
        self.value_label.config(text=f"£{total_value:.2f}")
        self.expiry_label.config(text=str(expiring_soon))
