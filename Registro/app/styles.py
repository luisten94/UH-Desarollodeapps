import tkinter as tk
from tkinter import ttk

def init_styles(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
    style.configure("H2.TLabel", font=("Segoe UI", 12, "bold"))
    style.configure("Brand.TLabel", font=("Segoe UI", 16, "bold"))
    style.configure("KPI.TLabel", font=("Segoe UI", 24, "bold"))
    style.configure("Card.TFrame", relief="groove")
