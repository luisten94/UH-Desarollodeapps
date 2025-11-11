import tkinter as tk
from tkinter import ttk

class SimpleLabelPage(ttk.Frame):
    """
    Página simple reutilizable para secciones que aún no tienen implementación.
    """
    def __init__(self, master, text: str):
        super().__init__(master, padding=16)
        ttk.Label(self, text=text, style="H2.TLabel")\
            .pack(anchor="w")
