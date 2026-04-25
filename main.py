import tkinter as tk
from tkinter import ttk
import json

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
tk.Label(top_frame, text="Value: £0").pack(side="left", padx=20)

menu_frame = tk.Frame(root, bg="lightgrey", width=150)
menu_frame.pack(side="left", fill="y")
menu_frame.pack_propagate(False)  
tk.Button(menu_frame, text="Dashboard").pack(fill="x", pady=5)
tk.Button(menu_frame, text="Add Product").pack(fill="x", pady=5)
tk.Button(menu_frame, text="Remove Product").pack(fill="x", pady=5)
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
