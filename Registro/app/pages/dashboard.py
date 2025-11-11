import tkinter as tk
from tkinter import ttk, messagebox

class DashboardPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)

        ttk.Label(self, text="Resumen del día", style="H2.TLabel")\
            .grid(row=0, column=0, columnspan=3, sticky="w")

        # Tarjetas KPI (ejemplo)
        self._kpi("Citas de hoy", "0", 1, 0)
        self._kpi("Vacunas pendientes", "0", 1, 1)
        self._kpi("Pacientes nuevos", "0", 1, 2)

        # Botones principales
        btn_login = ttk.Button(
            self,
            text="Iniciar sesión",
            command=self._go_login,
            width=20
        )
        btn_login.grid(row=2, column=0, pady=(20, 0), sticky="w")

        btn_reg_masc = ttk.Button(
            self,
            text="Registrar mascota",
            command=self._go_pet_register,
            width=20
        )
        btn_reg_masc.grid(row=2, column=1, pady=(20, 0), sticky="w")

        btn_reg_user = ttk.Button(
            self,
            text="Registrarme (usuario)",
            command=self._go_register_user,
            width=22
        )
        btn_reg_user.grid(row=2, column=2, pady=(20, 0), sticky="w")

        for c in range(3):
            self.columnconfigure(c, weight=1)

    def _kpi(self, title, value, r, c):
        card = ttk.Frame(self, padding=12, style="Card.TFrame")
        ttk.Label(card, text=title).grid(row=0, column=0, sticky="w")
        ttk.Label(card, text=value, style="KPI.TLabel").grid(row=1, column=0, sticky="w")
        card.grid(row=r, column=c, padx=(0, 12), pady=(12, 0), sticky="nwe")

    def _go_login(self):
        root = self.winfo_toplevel()
        if hasattr(root, "navigate"):
            root.navigate("login")

    def _go_pet_register(self):
        root = self.winfo_toplevel()
        # Si no estás autenticado, MainApp.navigate bloquea y avisa
        if hasattr(root, "navigate"):
            root.navigate("pet_register")

    def _go_register_user(self):
        root = self.winfo_toplevel()
        if hasattr(root, "navigate"):
            root.navigate("users")
