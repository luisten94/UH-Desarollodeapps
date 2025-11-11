import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from app.db import init_db, email_exists, insert_user
from app.security import pbkdf2_hash
from app.validators import is_valid_email, is_valid_cr_phone, normalize_phone, password_strength

ROLES = ("Dueno", "Veterinario", "Recepcion", "Admin")

class RegistroApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=16)
        master.title("TICOPET – Registro de Usuario")
        master.geometry("820x680")
        master.minsize(800, 640)
        self.pack(fill="both", expand=True)

        self._build_styles()
        self._build_form()

    def _build_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Warn.TLabel", foreground="#b00020")
        style.configure("OK.TLabel", foreground="#006400")

    def _build_form(self):
        header = ttk.Label(self, text="Registro de usuario TICOPET", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        # Variables
        self.var_rol = tk.StringVar(value=ROLES[0])
        self.var_nombre = tk.StringVar()
        self.var_apellidos = tk.StringVar()
        self.var_ident = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_tel = tk.StringVar()
        self.var_dir = tk.StringVar()
        self.var_pwd = tk.StringVar()
        self.var_pwd2 = tk.StringVar()
        self.var_show_pwd = tk.BooleanVar(value=False)
        self.var_terms = tk.BooleanVar(value=False)
        self.var_marketing = tk.BooleanVar(value=False)
        self.var_whatsapp = tk.BooleanVar(value=True)

        # Columna izquierda
        ttk.Label(self, text="Rol").grid(row=1, column=0, sticky="w", pady=(6, 2))
        self.cb_rol = ttk.Combobox(self, textvariable=self.var_rol, values=ROLES, state="readonly")
        self.cb_rol.grid(row=2, column=0, sticky="we", padx=(0, 12))

        ttk.Label(self, text="Nombre").grid(row=3, column=0, sticky="w", pady=(6, 2))
        self.ent_nombre = ttk.Entry(self, textvariable=self.var_nombre)
        self.ent_nombre.grid(row=4, column=0, sticky="we", padx=(0, 12))

        ttk.Label(self, text="Apellidos").grid(row=5, column=0, sticky="w", pady=(6, 2))
        self.ent_apellidos = ttk.Entry(self, textvariable=self.var_apellidos)
        self.ent_apellidos.grid(row=6, column=0, sticky="we", padx=(0, 12))

        ttk.Label(self, text="Identificación (opcional)").grid(row=7, column=0, sticky="w", pady=(6, 2))
        self.ent_ident = ttk.Entry(self, textvariable=self.var_ident)
        self.ent_ident.grid(row=8, column=0, sticky="we", padx=(0, 12))

        ttk.Label(self, text="Correo electrónico").grid(row=9, column=0, sticky="w", pady=(6, 2))
        self.ent_email = ttk.Entry(self, textvariable=self.var_email)
        self.ent_email.grid(row=10, column=0, sticky="we", padx=(0, 12))
        self.ent_email.bind("<FocusOut>", self._check_email_dup)

        # Columna central
        ttk.Label(self, text="Teléfono (CR)").grid(row=3, column=1, sticky="w", pady=(6, 2))
        self.ent_tel = ttk.Entry(self, textvariable=self.var_tel)
        self.ent_tel.grid(row=4, column=1, sticky="we", padx=(0, 12))

        ttk.Label(self, text="Dirección").grid(row=5, column=1, sticky="w", pady=(6, 2))
        self.ent_dir = ttk.Entry(self, textvariable=self.var_dir)
        self.ent_dir.grid(row=6, column=1, sticky="we", padx=(0, 12))

        ttk.Label(self, text="Contraseña").grid(row=7, column=1, sticky="w", pady=(6, 2))
        self.ent_pwd = ttk.Entry(self, textvariable=self.var_pwd, show="*")
        self.ent_pwd.grid(row=8, column=1, sticky="we", padx=(0, 12))
        self.ent_pwd.bind("<KeyRelease>", self._update_pwd_strength)

        ttk.Label(self, text="Confirmar contraseña").grid(row=9, column=1, sticky="w", pady=(6, 2))
        self.ent_pwd2 = ttk.Entry(self, textvariable=self.var_pwd2, show="*")
        self.ent_pwd2.grid(row=10, column=1, sticky="we", padx=(0, 12))

        self.chk_show = ttk.Checkbutton(self, text="Mostrar contraseña", variable=self.var_show_pwd, command=self._toggle_pwd)
        self.chk_show.grid(row=11, column=1, sticky="w", pady=(2, 8))

        # Indicador de contraseña
        self.lbl_pwd_strength = ttk.Label(self, text="Fuerza: -", style="Warn.TLabel")
        self.lbl_pwd_strength.grid(row=12, column=1, sticky="w", pady=(0, 8))

        # Columna derecha (preferencias)
        frm_opts = ttk.LabelFrame(self, text="Preferencias")
        frm_opts.grid(row=3, column=2, rowspan=6, sticky="nwe", padx=(0, 0))
        frm_opts.columnconfigure(0, weight=1)

        ttk.Checkbutton(frm_opts, text="Aceptar Términos y Política", variable=self.var_terms).grid(row=0, column=0, sticky="w", pady=(4, 2), padx=8)
        ttk.Checkbutton(frm_opts, text="Recibir comunicaciones (email)", variable=self.var_marketing).grid(row=1, column=0, sticky="w", pady=2, padx=8)
        ttk.Checkbutton(frm_opts, text="Recordatorios por WhatsApp/SMS", variable=self.var_whatsapp).grid(row=2, column=0, sticky="w", pady=2, padx=8)

        # Barra inferior de acciones
        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=13, column=0, columnspan=4, sticky="ew", pady=10)

        btn_reg = ttk.Button(self, text="Registrar", command=self._submit)
        btn_limpiar = ttk.Button(self, text="Limpiar", command=self._clear)
        btn_salir = ttk.Button(self, text="Salir", command=self._quit)

        btn_reg.grid(row=14, column=0, sticky="w", pady=6)
        btn_limpiar.grid(row=14, column=1, sticky="w", pady=6)
        btn_salir.grid(row=14, column=2, sticky="w", pady=6)

        # Layout
        for c in range(3):
            self.columnconfigure(c, weight=1)
        self.rowconfigure(99, weight=1)

        # Atajo: Ctrl+Enter para registrar
        self.bind_all("<Control-Return>", lambda e: self._submit())

    # ---------- Interacciones ----------
    def _toggle_pwd(self):
        show = "" if self.var_show_pwd.get() else "*"
        self.ent_pwd.config(show=show)
        self.ent_pwd2.config(show=show)

    def _update_pwd_strength(self, event=None):
        name = self.var_nombre.get().strip()
        last = self.var_apellidos.get().strip()
        mail = self.var_email.get().strip()
        local_part = mail.split("@")[0] if "@" in mail else mail
        score, tips = password_strength(self.var_pwd.get(), [name, last, local_part])
        labels = {
            0: ("Muy débil", "Warn.TLabel"),
            1: ("Muy débil", "Warn.TLabel"),
            2: ("Débil", "Warn.TLabel"),
            3: ("Aceptable", "TLabel"),
            4: ("Buena", "OK.TLabel"),
            5: ("Fuerte", "OK.TLabel"),
            6: ("Excelente", "OK.TLabel"),
        }
        txt, sty = labels.get(score, ("-", "TLabel"))
        self.lbl_pwd_strength.config(text=f"Fuerza: {txt}", style=sty)

    def _check_email_dup(self, event=None):
        email = self.var_email.get().strip()
        if email and is_valid_email(email) and email_exists(email):
            messagebox.showwarning("Correo ya registrado", "El correo ingresado ya existe. Usa otro o recupera tu contraseña.")

    def _clear(self):
        self.var_rol.set(ROLES[0])
        self.var_nombre.set("")
        self.var_apellidos.set("")
        self.var_ident.set("")
        self.var_email.set("")
        self.var_tel.set("")
        self.var_dir.set("")
        self.var_pwd.set("")
        self.var_pwd2.set("")
        self.var_show_pwd.set(False)
        self.var_terms.set(False)
        self.var_marketing.set(False)
        self.var_whatsapp.set(True)
        self._update_pwd_strength()

    def _quit(self):
        self.master.destroy()

    def _submit(self):
        # Recolectar
        rol = self.var_rol.get().strip()
        nombre = self.var_nombre.get().strip()
        apellidos = self.var_apellidos.get().strip()
        identificacion = self.var_ident.get().strip() or None
        email = self.var_email.get().strip().lower()
        telefono_raw = self.var_tel.get().strip()
        telefono = normalize_phone(telefono_raw)
        direccion = self.var_dir.get().strip() or None
        pwd = self.var_pwd.get()
        pwd2 = self.var_pwd2.get()
        terms = self.var_terms.get()
        marketing = self.var_marketing.get()
        whatsapp = self.var_whatsapp.get()

        # Validaciones
        if rol not in ROLES:
            return messagebox.showerror("Dato inválido", "Selecciona un rol válido.")
        if not nombre:
            return messagebox.showerror("Dato requerido", "El nombre es obligatorio.")
        if not apellidos:
            return messagebox.showerror("Dato requerido", "Los apellidos son obligatorios.")
        if not email or not is_valid_email(email):
            return messagebox.showerror("Correo inválido", "Ingresa un correo válido.")
        if email_exists(email):
            return messagebox.showerror("Correo duplicado", "Este correo ya está registrado.")
        if not telefono or not is_valid_cr_phone(telefono):
            return messagebox.showerror("Teléfono inválido", "Ingresa un teléfono de Costa Rica (8 dígitos).")
        if not pwd or not pwd2:
            return messagebox.showerror("Contraseña requerida", "Completa ambos campos de contraseña.")
        if pwd != pwd2:
            return messagebox.showerror("No coinciden", "Las contraseñas no coinciden.")

        local_part = email.split("@")[0]
        score, tips = password_strength(pwd, [nombre, apellidos, local_part])
        if score < 4:
            return messagebox.showerror("Contraseña débil", "\n".join(["Mejora tu contraseña:"] + tips))
        if not terms:
            return messagebox.showerror("Términos", "Debes aceptar los términos y la política para continuar.")

        # Insertar
        pwd_hash, salt = pbkdf2_hash(pwd)
        now = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        data = {
            "rol": rol,
            "nombre": nombre,
            "apellidos": apellidos,
            "identificacion": identificacion,
            "email": email,
            "telefono": telefono,
            "direccion": direccion,
            "password_hash": pwd_hash,
            "salt": salt,
            "terms_accepted": terms,
            "marketing_opt_in": marketing,
            "whatsapp_opt_in": whatsapp,
            "created_at": now,
            "updated_at": now,
        }

        try:
            user_id = insert_user(data)
        except Exception as e:
            return messagebox.showerror("Error", f"Ocurrió un error al registrar: {e}")

        messagebox.showinfo("Registro exitoso", f"Usuario creado con ID #{user_id}.")
        self._clear()

def main() -> None:
    init_db()
    root = tk.Tk()
    app = RegistroApp(root)
    root.mainloop()
