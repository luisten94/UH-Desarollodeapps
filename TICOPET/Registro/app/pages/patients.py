import tkinter as tk
from tkinter import ttk, messagebox

class PatientsPage(ttk.Frame):
    """
    Página de listado de pacientes.
    Por ahora usa datos de ejemplo.
    """
    def __init__(self, master):
        super().__init__(master, padding=16)

        ttk.Label(self, text="Pacientes", style="H2.TLabel")\
            .grid(row=0, column=0, sticky="w")

        self.tree = ttk.Treeview(
            self,
            columns=("nombre", "especie", "raza", "dueno"),
            show="headings",
            height=18
        )

        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("especie", text="Especie")
        self.tree.heading("raza", text="Raza")
        self.tree.heading("dueno", text="Dueño")

        for c in ("nombre", "especie", "raza", "dueno"):
            self.tree.column(c, width=150, anchor="w")

        self.tree.grid(row=1, column=0, columnspan=2,
                       sticky="nsew", pady=(8, 8))

        btns = ttk.Frame(self)
        btns.grid(row=2, column=0, sticky="w")

        ttk.Button(btns, text="+ Nuevo", command=self._nuevo)\
            .pack(side="left", padx=(0, 6))
        ttk.Button(btns, text="Editar", command=self._editar)\
            .pack(side="left", padx=6)
        ttk.Button(btns, text="Eliminar", command=self._eliminar)\
            .pack(side="left", padx=6)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self._load_mock()

    def _load_mock(self):
        demo = [
            ("Luna", "Canino", "Labrador", "María Gómez"),
            ("Mishi", "Felino", "Siamés", "Carlos Pérez"),
        ]
        for row in demo:
            self.tree.insert("", "end", values=row)

    def _sel(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pacientes", "Seleccione un paciente.")
            return None
        return sel[0], self.tree.item(sel[0], "values")

    def _nuevo(self):
        root = self.winfo_toplevel()
        if hasattr(root, "navigate"):
            root.navigate("pet_register")

    def _editar(self):
        s = self._sel()
        if s:
            _, values = s
            messagebox.showinfo("Pacientes", f"Editar paciente: {values[0]} (demo)")

    def _eliminar(self):
        s = self._sel()
        if s:
            iid, values = s
            if messagebox.askyesno("Confirmar", f"¿Eliminar {values[0]}? (demo)"):
                self.tree.delete(iid)
