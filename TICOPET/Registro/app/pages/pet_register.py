import tkinter as tk
from tkinter import ttk, messagebox
from app import db_pets

class PetRegisterPage(ttk.Frame):
    """
    Pantalla de registro de mascota.
    Guarda en la tabla 'mascotas' de ticopet.db.
    Si hay usuario logueado, guarda en 'registrado_por'.
    """
    def __init__(self, master):
        super().__init__(master, padding=16)

        ttk.Label(self, text="Registro de mascota", style="H2.TLabel")\
            .grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        row = 1

        # Nombre
        ttk.Label(self, text="Nombre").grid(row=row, column=0, sticky="w", pady=4)
        self.nombre_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.nombre_var, width=25)\
            .grid(row=row, column=1, sticky="w", pady=4)

        # Especie
        ttk.Label(self, text="Especie").grid(row=row, column=2, sticky="w", pady=4)
        self.especie_var = tk.StringVar()
        cb_especie = ttk.Combobox(
            self,
            textvariable=self.especie_var,
            values=["Canino", "Felino", "Ave", "Reptil", "Otro"],
            state="readonly",
            width=15
        )
        cb_especie.grid(row=row, column=3, sticky="w", pady=4)
        cb_especie.current(0)

        row += 1

        # Raza
        ttk.Label(self, text="Raza").grid(row=row, column=0, sticky="w", pady=4)
        self.raza_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.raza_var, width=25)\
            .grid(row=row, column=1, sticky="w", pady=4)

        # Sexo
        ttk.Label(self, text="Sexo").grid(row=row, column=2, sticky="w", pady=4)
        self.sexo_var = tk.StringVar()
        cb_sexo = ttk.Combobox(
            self,
            textvariable=self.sexo_var,
            values=["Macho", "Hembra"],
            state="readonly",
            width=15
        )
        cb_sexo.grid(row=row, column=3, sticky="w", pady=4)
        cb_sexo.current(0)

        row += 1

        # Edad
        ttk.Label(self, text="Edad (años)").grid(row=row, column=0, sticky="w", pady=4)
        self.edad_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.edad_var, width=10)\
            .grid(row=row, column=1, sticky="w", pady=4)

        # Peso
        ttk.Label(self, text="Peso (kg)").grid(row=row, column=2, sticky="w", pady=4)
        self.peso_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.peso_var, width=10)\
            .grid(row=row, column=3, sticky="w", pady=4)

        row += 1

        # Color
        ttk.Label(self, text="Color").grid(row=row, column=0, sticky="w", pady=4)
        self.color_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.color_var, width=25)\
            .grid(row=row, column=1, sticky="w", pady=4)

        # Dueño
        ttk.Label(self, text="Dueño").grid(row=row, column=2, sticky="w", pady=4)
        self.dueno_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.dueno_var, width=20)\
            .grid(row=row, column=3, sticky="w", pady=4)

        row += 1

        # Contacto
        ttk.Label(self, text="Contacto dueño").grid(row=row, column=0, sticky="w", pady=4)
        self.contacto_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.contacto_var, width=25)\
            .grid(row=row, column=1, sticky="w", pady=4)

        row += 1

        # Observaciones
        ttk.Label(self, text="Observaciones").grid(row=row, column=0, sticky="nw", pady=4)
        self.obs_txt = tk.Text(self, width=50, height=4)
        self.obs_txt.grid(row=row, column=1, columnspan=3, sticky="w", pady=4)

        row += 1

        # Botones
        btns = ttk.Frame(self)
        btns.grid(row=row, column=0, columnspan=4, sticky="w", pady=(12, 0))
        ttk.Button(btns, text="Guardar", command=self._guardar)\
            .pack(side="left")
        ttk.Button(btns, text="Limpiar", command=self._limpiar)\
            .pack(side="left", padx=8)

        for c in range(4):
            self.columnconfigure(c, weight=1)

    def _guardar(self):
        nombre = self.nombre_var.get().strip()
        especie = self.especie_var.get().strip()
        raza = self.raza_var.get().strip()
        sexo = self.sexo_var.get().strip()
        edad = self.edad_var.get().strip()
        peso = self.peso_var.get().strip()
        color = self.color_var.get().strip()
        dueno = self.dueno_var.get().strip()
        contacto = self.contacto_var.get().strip()
        observaciones = self.obs_txt.get("1.0", "end").strip()

        # Validaciones mínimas
        if not nombre:
            messagebox.showwarning("Registro mascota", "El nombre de la mascota es obligatorio.")
            return
        if not especie:
            messagebox.showwarning("Registro mascota", "La especie es obligatoria.")
            return
        if not dueno:
            messagebox.showwarning("Registro mascota", "Debe indicar el dueño.")
            return

        # Obtener el usuario autenticado desde la ventana principal (si existe)
        root = self.winfo_toplevel()
        registrado_por = getattr(root, "current_user", None)

        try:
            db_pets.create_pet(
                nombre=nombre,
                especie=especie,
                raza=raza,
                sexo=sexo,
                edad=edad,
                peso=peso,
                color=color,
                dueno=dueno,
                contacto=contacto,
                observaciones=observaciones,
                registrado_por=registrado_por
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo guardar la mascota.\nDetalle: {e}"
            )
            return

        messagebox.showinfo(
            "Registro mascota",
            f"Mascota '{nombre}' registrada correctamente."
        )
        self._limpiar()

    def _limpiar(self):
        self.nombre_var.set("")
        self.especie_var.set("Canino")
        self.raza_var.set("")
        self.sexo_var.set("Macho")
        self.edad_var.set("")
        self.peso_var.set("")
        self.color_var.set("")
        self.dueno_var.set("")
        self.contacto_var.set("")
        self.obs_txt.delete("1.0", "end")
