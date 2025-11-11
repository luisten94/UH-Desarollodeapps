import re
from typing import List, Tuple, Optional

def is_valid_email(email: str) -> bool:
    pattern = r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$"
    return re.match(pattern, email.strip(), re.IGNORECASE) is not None

def normalize_phone(phone: str) -> str:
    """Deja solo dígitos. Si empieza con 506 y sobran, quita el 506."""
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("506") and len(digits) > 8:
        digits = digits[3:]
    return digits

def is_valid_cr_phone(phone: str) -> bool:
    """Costa Rica: exactamente 8 dígitos tras normalizar."""
    digits = normalize_phone(phone)
    return len(digits) == 8

def password_strength(password: str, forbidden: Optional[List[str]] = None) -> Tuple[int, List[str]]:
    """
    Devuelve (score 0-6, tips).
    Puntos por: longitud>=10, minúsculas, mayúsculas, dígitos, símbolo, no contener partes del nombre/correo.
    """
    tips: List[str] = []
    score = 0

    if len(password) >= 10:
        score += 1
    else:
        tips.append("Usa al menos 10 caracteres")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        tips.append("Incluye minúsculas")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        tips.append("Incluye mayúsculas")

    if re.search(r"\d", password):
        score += 1
    else:
        tips.append("Incluye dígitos")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        tips.append("Incluye un símbolo (p. ej. !@#)")

    if forbidden:
        for f in forbidden:
            if f and f.lower() in password.lower():
                tips.append("No uses partes de tu nombre/correo en la contraseña")
                break
        else:
            score += 1
    else:
        score += 1

    return score, tips
