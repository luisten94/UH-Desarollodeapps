import tkinter as tk
from tkinter import ttk, messagebox
from app import db_vets

class VetRegisterPage(ttk.Frame):
    """
    Registro de veterinario en 'veterinarios' (ticopet.db).
    Guarda 'registrado_por' si hay usuario logueado (MainApp.current_user).
    """
    def __init__(self, master):
        super().__init__(master, padding=16)

        ttk.Label(self, text="Registro de veterinario", style="H2.TLabel")\
            .grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        row = 1

        # Nombre
        ttk.Label(self, text="Nombre completo").grid(row=row, column=0, sticky="w", pady=4)
        self.nombre_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.nombre_var, width=28).grid(row=row, column=1, sticky="w", pady=4)

        # Colegiado (único)
        ttk.Label(self, text="N.º Colegiado").grid(row=row, column=2, sticky="w", pady=4)
        self.colegiado_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.colegiado_var, width=18).grid(row=row, column=3, sticky="w", pady=4)

        row += 1

        # Cédula
        ttk.Label(self, text="Cédula").grid(row=row, column=0, sticky="w", pady=4)
        self.cedula_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.cedula_var, width=28).grid(row=row, column=1, sticky="w", pady=4)

        # Especialidad
        ttk.Label(self, text="Especialidad").grid(row=row, column=2, sticky="w", pady=4)
        self.especialidad_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.especialidad_var, width=18).grid(row=row, column=3, sticky="w", pady=4)

        row += 1

        # Teléfono
        ttk.Label(self, text="Teléfono").grid(row=row, column=0, sticky="w", pady=4)
        self.telefono_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.telefono_var, width=28).grid(row=row, column=1, sticky="w", pady=4)

        # Correo
        ttk.Label(self, text="Correo").grid(row=row, column=2, sticky="w", pady=4)
        self.correo_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.correo_var, width=18).grid(row=row, column=3, sticky="w", pady=4)

        row += 1

        # Dirección
        ttk.Label(self, text="Dirección").grid(row=row, column=0, sticky="nw", pady=4)
        self.direccion_txt = tk.Text(self, width=50, height=3)
        self.direccion_txt.grid(row=row, column=1, columnspan=3, sticky="w", pady=4)

        row += 1

        # Observaciones
        ttk.Label(self, text="Observaciones").grid(row=row, column=0, sticky="nw", pady=4)
        self.obs_txt = tk.Text(self, width=50, height=3)
        self.obs_txt.grid(row=row, column=1, columnspan=3, sticky="w", pady=4)

        row += 1

        # Botones
        btns = ttk.Frame(self)
        btns.grid(row=row, column=0, columnspan=4, sticky="w", pady=(12, 0))
        ttk.Button(btns, text="Guardar", command=self._guardar).pack(side="left")
        ttk.Button(btns, text="Limpiar", command=self._limpiar).pack(side="left", padx=8)

        for c in range(4):
            self.columnconfigure(c, weight=1)

    def _guardar(self):
        nombre = self.nombre_var.get().strip()
        colegiado = self.colegiado_var.get().strip()
        cedula = self.cedula_var.get().strip()
        especialidad = self.especialidad_var.get().strip()
        telefono = self.telefono_var.get().strip()
        correo = self.correo_var.get().strip()
        direccion = self.direccion_txt.get("1.0", "end").strip()
        observaciones = self.obs_txt.get("1.0", "end").strip()

        # Validaciones mínimas
        if not nombre:
            messagebox.showwarning("Veterinarios", "El nombre es obligatorio.")
            return
        if not colegiado:
            messagebox.showwarning("Veterinarios", "El N.º de colegiado es obligatorio.")
            return

        # Usuario autenticado (si lo hay)
        root = self.winfo_toplevel()
        registrado_por = getattr(root, "current_user", None)

        ok = db_vets.create_vet(
            nombre=nombre,
            colegiado=colegiado,
            cedula=cedula or None,
            especialidad=especialidad or None,
            telefono=telefono or None,
            correo=correo or None,
            direccion=direccion or None,
            observaciones=observaciones or None,
            registrado_por=registrado_por
        )

        if not ok:
            messagebox.showerror(
                "Veterinarios",
                "Ese N.º de colegiado ya existe. Verifique los datos."
            )
            return

        messagebox.showinfo("Veterinarios", "Veterinario registrado correctamente.")
        self._limpiar()

    def _limpiar(self):
        self.nombre_var.set("")
        self.colegiado_var.set("")
        self.cedula_var.set("")
        self.especialidad_var.set("")
        self.telefono_var.set("")
        self.correo_var.set("")
        self.direccion_txt.delete("1.0", "end")
        self.obs_txt.delete("1.0", "end")
