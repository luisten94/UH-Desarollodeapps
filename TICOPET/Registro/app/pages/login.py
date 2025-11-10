import tkinter as tk
from tkinter import ttk, messagebox
from app import db_users

class LoginPage(ttk.Frame):
    """
    Pantalla de inicio de sesión usando la tabla 'usuarios' de ticopet.db.
    """
    def __init__(self, master):
        super().__init__(master, padding=16)

        ttk.Label(self, text="Iniciar sesión", style="H2.TLabel")\
            .grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ttk.Label(self, text="Usuario").grid(row=1, column=0, sticky="w", pady=4)
        self.user_var = tk.StringVar()
        self.entry_user = ttk.Entry(self, textvariable=self.user_var, width=30)
        self.entry_user.grid(row=1, column=1, sticky="w", pady=4)

        ttk.Label(self, text="Contraseña").grid(row=2, column=0, sticky="w", pady=4)
        self.pass_var = tk.StringVar()
        self.entry_pass = ttk.Entry(self, textvariable=self.pass_var, show="*", width=30)
        self.entry_pass.grid(row=2, column=1, sticky="w", pady=4)

        ttk.Button(self, text="Entrar", command=self._login)\
            .grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        ttk.Button(self, text="Volver al Dashboard",
                   command=self._back_dashboard)\
            .grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))

        self.columnconfigure(1, weight=1)
        self.entry_user.focus()

        self.bind_all("<Return>", self._on_enter)

    def _on_enter(self, event):
        if self.winfo_ismapped():
            self._login()

    def _login(self):
        user = self.user_var.get().strip()
        password = self.pass_var.get().strip()

        if not user or not password:
            messagebox.showwarning("Login", "Complete usuario y contraseña.")
            return

        if db_users.validate_user(user, password):
            root = self.winfo_toplevel()
            if hasattr(root, "set_authenticated"):
                root.set_authenticated(user)
            else:
                messagebox.showerror("Error", "No se pudo establecer la sesión.")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            self.pass_var.set("")
            self.entry_pass.focus()

    def _back_dashboard(self):
        root = self.winfo_toplevel()
        if hasattr(root, "navigate"):
            root.navigate("dashboard")
