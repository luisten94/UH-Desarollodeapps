import tkinter as tk
from tkinter import ttk, messagebox

from app.styles import init_styles
from app.pages.dashboard import DashboardPage
from app.pages.patients import PatientsPage
from app.pages.simple import SimpleLabelPage
from app.pages.users import UsersPage
from app.pages.login import LoginPage
from app.pages.pet_register import PetRegisterPage
from app.pages.vet_register import VetRegisterPage

APP_NAME = "TicoVet"

class Sidebar(ttk.Frame):
    def __init__(self, master, on_nav):
        super().__init__(master, padding=(8, 12))
        self.on_nav = on_nav
        self.buttons = {}
        self._build()

    def _btn(self, text, key):
        btn = ttk.Button(self, text=text, command=lambda: self.on_nav(key))
        btn.pack(fill="x", pady=3)
        self.buttons[key] = btn
        return btn

    def _build(self):
        ttk.Label(self, text=APP_NAME, style="Brand.TLabel")\
            .pack(fill="x", pady=(0, 10))

        self._btn("Dashboard", "dashboard")
        self._btn("Pacientes", "patients")
        self._btn("Registrar mascota", "pet_register")
        self._btn("Registrar veterinario", "vet_register")
        self._btn("Dueños", "owners")
        self._btn("Citas", "appointments")
        self._btn("Vacunas", "vaccines")
        self._btn("Inventario", "inventory")
        self._btn("Facturación", "billing")
        self._btn("Reportes", "reports")

        self._btn("Registro de usuario", "users")
        self._btn("Iniciar sesión", "login")

        ttk.Separator(self).pack(fill="x", pady=8)
        ttk.Button(self, text="Salir", command=self._exit).pack(fill="x")

    def _exit(self):
        root = self.winfo_toplevel()
        root.destroy()

    def set_protected_enabled(self, enabled: bool):
        """
        Habilita o deshabilita las secciones que requieren sesión.
        """
        protegidos = [
            "patients", "pet_register", "owners", "appointments",
            "vaccines", "inventory", "billing", "reports"
        ]
        state = "normal" if enabled else "disabled"
        for key in protegidos:
            if key in self.buttons:
                self.buttons[key]["state"] = state

class TopBar(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(12, 8))
        self.columnconfigure(1, weight=1)
        self.title_lbl = ttk.Label(self, text="Dashboard", style="Title.TLabel")
        self.title_lbl.grid(row=0, column=0, sticky="w")

    def set_title(self, text):
        self.title_lbl.configure(text=text)

class StatusBar(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(1, weight=1)
        self.user_lbl = ttk.Label(self, text="Usuario: (no autenticado)")
        self.msg_lbl = ttk.Label(self, text="")
        self.user_lbl.grid(row=0, column=0, padx=8, pady=4, sticky="w")
        self.msg_lbl.grid(row=0, column=1, padx=8, pady=4, sticky="e")

    def set_user(self, username: str | None):
        if username:
            self.user_lbl.configure(text=f"Usuario: {username}")
        else:
            self.user_lbl.configure(text="Usuario: (no autenticado)")

    def set_message(self, text: str):
        self.msg_lbl.configure(text=text)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} - Gestión Veterinaria")
        self.geometry("1100x680")
        self.minsize(980, 600)

        init_styles(self)

        self.current_user = None
        self.is_authenticated = False

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(1, weight=1)

        self.sidebar = Sidebar(container, self.navigate)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsw")

        self.topbar = TopBar(container)
        self.topbar.grid(row=0, column=1, sticky="new")

        self.content = ttk.Frame(container)
        self.content.grid(row=1, column=1, sticky="nsew")

        self.status = StatusBar(self)
        self.status.pack(fill="x", side="bottom")

        # Inicializar páginas
        self.pages = {
            "dashboard":    DashboardPage(self.content),
            "patients":     PatientsPage(self.content),
            "pet_register": PetRegisterPage(self.content),
            "owners":       SimpleLabelPage(self.content, "Gestión de dueños"),
            "appointments": SimpleLabelPage(self.content, "Agenda de citas"),
            "vaccines":     SimpleLabelPage(self.content, "Control de vacunas"),
            "inventory":    SimpleLabelPage(self.content, "Inventario"),
            "billing":      SimpleLabelPage(self.content, "Facturación"),
            "reports":      SimpleLabelPage(self.content, "Reportes"),
            "users":        UsersPage(self.content),   # registro de usuario
            "login":        LoginPage(self.content),   # inicio de sesión
            "settings":     SimpleLabelPage(self.content, "Ajustes"),
            "vet_register":  VetRegisterPage(self.content),
        }

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Al inicio las secciones protegidas deshabilitadas
        self.sidebar.set_protected_enabled(False)

        # Mostrar pantalla principal (Dashboard)
        self.navigate("dashboard")

        self._bind_shortcuts()

    def _bind_shortcuts(self):
        self.bind_all("<Control-d>", lambda e: self.navigate("dashboard"))
        self.bind_all("<Control-l>", lambda e: self.navigate("login"))
        self.bind_all("<Control-u>", lambda e: self.navigate("users"))

    def navigate(self, key: str):
        if key not in self.pages:
            return

        publicas = {"dashboard", "login", "users"}

        # Si no está autenticado, solo puede ver públicas
        if (not self.is_authenticated) and key not in publicas:
            messagebox.showwarning(
                "Acceso restringido",
                "Debes registrarte o iniciar sesión para acceder a esta sección."
            )
            key = "dashboard"

        for name, page in self.pages.items():
            if name == key:
                page.lift()
            else:
                page.lower()

        titulos = {
            "dashboard": "Dashboard",
            "patients": "Pacientes",
            "pet_register": "Registro de mascota",
            "vet_register": "Registro de veterinario",
            "owners": "Dueños",
            "appointments": "Citas",
            "vaccines": "Vacunas",
            "inventory": "Inventario",
            "billing": "Facturación",
            "reports": "Reportes",
            "users": "Registro de usuario",
            "login": "Iniciar sesión",
            "settings": "Ajustes",
        }
        self.topbar.set_title(titulos.get(key, "Panel"))

    def set_authenticated(self, username: str):
        """
        Llamado por LoginPage cuando el login es correcto.
        Activa secciones protegidas.
        """
        self.is_authenticated = True
        self.current_user = username
        self.status.set_user(username)
        self.status.set_message("Sesión iniciada correctamente.")
        self.sidebar.set_protected_enabled(True)
        self.navigate("dashboard")
