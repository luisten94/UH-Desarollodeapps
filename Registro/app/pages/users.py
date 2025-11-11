import tkinter as tk
from tkinter import ttk, messagebox
from app import db_users  # usa ticopet.db

class UsersPage(ttk.Frame):
    """
    Página de registro de usuario.
    Guarda los datos en la tabla 'usuarios' de ticopet.db usando db_users.py.
    """
    def __init__(self, master):
        super().__init__(master, padding=16)

        ttk.Label(self, text="Registro de usuario", style="H2.TLabel")\
            .grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        form = ttk.Frame(self)
        form.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Nombre completo
        ttk.Label(form, text="Nombre completo").grid(row=0, column=0, sticky="w", pady=4)
        self.nombre_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.nombre_var, width=32)\
            .grid(row=0, column=1, sticky="w", pady=4)

        # Usuario (único)
        ttk.Label(form, text="Usuario").grid(row=1, column=0, sticky="w", pady=4)
        self.user_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.user_var, width=32)\
            .grid(row=1, column=1, sticky="w", pady=4)

        # Correo
        ttk.Label(form, text="Correo").grid(row=2, column=0, sticky="w", pady=4)
        self.email_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.email_var, width=32)\
            .grid(row=2, column=1, sticky="w", pady=4)

        # Contraseña
        ttk.Label(form, text="Contraseña").grid(row=3, column=0, sticky="w", pady=4)
        self.pass1_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.pass1_var, show="*", width=32)\
            .grid(row=3, column=1, sticky="w", pady=4)

        # Confirmar contraseña
        ttk.Label(form, text="Confirmar contraseña").grid(row=4, column=0, sticky="w", pady=4)
        self.pass2_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.pass2_var, show="*", width=32)\
            .grid(row=4, column=1, sticky="w", pady=4)

        # Botones
        btns = ttk.Frame(self)
        btns.grid(row=2, column=0, columnspan=2, sticky="w", pady=(12, 0))

        ttk.Button(btns, text="Guardar", command=self._guardar)\
            .pack(side="left")
        ttk.Button(btns, text="Limpiar", command=self._limpiar)\
            .pack(side="left", padx=8)

    def _guardar(self):
        nombre = self.nombre_var.get().strip()
        usuario = self.user_var.get().strip()
        correo = self.email_var.get().strip()
        p1 = self.pass1_var.get().strip()
        p2 = self.pass2_var.get().strip()

        # Validaciones básicas
        if not (nombre and usuario and correo and p1 and p2):
            messagebox.showwarning("Registro", "Complete todos los campos.")
            return

        if len(usuario) < 3:
            messagebox.showwarning("Registro", "El usuario debe tener al menos 3 caracteres.")
            return

        if p1 != p2:
            messagebox.showwarning("Registro", "Las contraseñas no coinciden.")
            return

        if len(p1) < 4:
            messagebox.showwarning("Registro", "La contraseña debe tener al menos 4 caracteres.")
            return

        # Guardar en BD (usa db_users.py)
        ok = db_users.create_user(nombre, usuario, correo, p1)

        if not ok:
            messagebox.showerror(
                "Registro",
                "Ese nombre de usuario ya existe. Elija otro."
            )
            return

        messagebox.showinfo(
            "Registro",
            "Usuario registrado correctamente. Ahora puede ir a 'Iniciar sesión'."
        )
        self._limpiar()

    def _limpiar(self):
        self.nombre_var.set("")
        self.user_var.set("")
        self.email_var.set("")
        self.pass1_var.set("")
        self.pass2_var.set("")
