import re
from werkzeug.security import generate_password_hash
import logging

# Setup logger per utility functions
utils_logger = logging.getLogger('auth_utils')
utils_logger.setLevel(logging.INFO)

def controllo_email(email):
    """
    Verifica se una stringa è un'email valida usando regex.

    Args:
        email (str): L'indirizzo email da validare.

    Returns:
        bool: True se l'email è valida, False altrimenti.

    Examples:
        >>> controllo_email("user@example.com")
        True
        >>> controllo_email("invalid-email")
        False

    References:
        [1] - Python regex patterns and email validation
    """
    if not email or not isinstance(email, str):
        return False

    # Pattern regex per validazione email
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    result = re.match(pattern, email) is not None

    # Log per debugging (solo in caso di validazione fallita)
    if not result:
        utils_logger.debug(f"Email validation failed for: {email[:10]}...")

    return result

def psw_proteggi_hash(psw):
    """
    Genera un hash sicuro per la password fornita usando Werkzeug.

    Args:
        psw (str): La password in chiaro.

    Returns:
        str: L'hash sicuro della password.

    Raises:
        ValueError: Se la password è vuota o None
        TypeError: Se la password non è una stringa

    Examples:
        >>> hash_password = psw_proteggi_hash("mypassword123")
        >>> len(hash_password) > 20  # Hash è sempre lungo
        True

    References:
        [2] - Werkzeug password hashing security
        [3] - Password hashing best practices
    """
    # Validazione input
    if not psw:
        raise ValueError("Password cannot be empty or None")

    if not isinstance(psw, str):
        raise TypeError(f"Password must be string, got {type(psw)}")

    try:
        # Genera hash sicuro usando Werkzeug
        hash_result = generate_password_hash(psw)

        # Log successful hashing (senza mostrare la password)
        utils_logger.debug(f"Password hashed successfully, hash length: {len(hash_result)}")

        return hash_result

    except Exception as e:
        utils_logger.error(f"Error hashing password: {str(e)}")
        raise

def valida_lunghezza_username(username, min_length=3, max_length=50):
    """
    Valida la lunghezza del nome utente.

    Args:
        username (str): Nome utente da validare
        min_length (int): Lunghezza minima (default: 3)
        max_length (int): Lunghezza massima (default: 50)

    Returns:
        tuple: (is_valid: bool, message: str)

    Examples:
        >>> valida_lunghezza_username("user")
        (True, "")
        >>> valida_lunghezza_username("ab")
        (False, "Nome utente troppo corto (minimo 3 caratteri)")

    References:
        [4] - Username validation standards
    """
    if not username or not isinstance(username, str):
        return False, "Nome utente è obbligatorio"

    username = username.strip()

    if len(username) < min_length:
        return False, f"Nome utente troppo corto (minimo {min_length} caratteri)"

    if len(username) > max_length:
        return False, f"Nome utente troppo lungo (massimo {max_length} caratteri)"

    # Controlla caratteri validi (lettere, numeri, underscore, trattino)
    if not re.match(r'^[\w\-]+$', username):
        return False, "Nome utente può contenere solo lettere, numeri, underscore e trattini"

    return True, ""

def sanitizza_input(input_string, max_length=None):
    """
    Sanitizza input utente rimuovendo spazi e caratteri pericolosi.

    Args:
        input_string (str): Stringa da sanitizzare
        max_length (int, optional): Lunghezza massima

    Returns:
        str: Stringa sanitizzata

    Examples:
        >>> sanitizza_input("  hello world  ")
        "hello world"
        >>> sanitizza_input("test<script>", max_length=6)
        "test"

    References:
        [5] - Input sanitization security
    """
    if not input_string:
        return ""

    # Rimuovi spazi iniziali e finali
    sanitized = str(input_string).strip()

    # Rimuovi caratteri potenzialmente pericolosi per XSS base
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')

    # Limita lunghezza se specificata
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
        utils_logger.warning(f"Input truncated to {max_length} characters")

    return sanitized

def valida_formato_password_base(password):
    """
    Validazione password base (versione semplificata per compatibilità).

    Args:
        password (str): Password da validare

    Returns:
        tuple: (is_valid: bool, message: str)

    Note:
        Questa è una versione semplificata. Per validazione avanzata,
        usa PasswordManager dal modulo password_manager.

    Examples:
        >>> valida_formato_password_base("Test123!")
        (True, "")
        >>> valida_formato_password_base("weak")
        (False, "Password troppo corta (minimo 8 caratteri)")

    References:
        [6] - Basic password security requirements
    """
    if not password:
        return False, "Password è obbligatoria"

    if len(password) < 8:
        return False, "Password troppo corta (minimo 8 caratteri)"

    if len(password) > 128:
        return False, "Password troppo lunga (massimo 128 caratteri)"

    # Controlli base
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    missing = []
    if not has_upper:
        missing.append("una lettera maiuscola")
    if not has_lower:
        missing.append("una lettera minuscola")
    if not has_digit:
        missing.append("un numero")

    if missing:
        return False, f"Password deve contenere almeno: {', '.join(missing)}"

    return True, ""

def formatta_messaggio_errore(errors_list, max_errors=3):
    """
    Formatta una lista di errori in un messaggio user-friendly.

    Args:
        errors_list (list): Lista di messaggi di errore
        max_errors (int): Numero massimo di errori da mostrare

    Returns:
        str: Messaggio formattato

    Examples:
        >>> errors = ["Email non valida", "Password troppo corta", "Username già in uso"]
        >>> formatta_messaggio_errore(errors, 2)
        "Email non valida; Password troppo corta (e 1 altro errore)"

    References:
        [7] - User-friendly error messaging
    """
    if not errors_list:
        return ""

    # Limita numero di errori mostrati
    shown_errors = errors_list[:max_errors]
    hidden_count = len(errors_list) - len(shown_errors)

    message = "; ".join(shown_errors)

    if hidden_count > 0:
        message += f" (e {hidden_count} altro{'i' if hidden_count > 1 else ''} error{'i' if hidden_count > 1 else 'e'})"

    return message

def genera_username_suggerimenti(base_name, existing_usernames=None):
    """
    Genera suggerimenti di username disponibili basati su un nome base.

    Args:
        base_name (str): Nome base per i suggerimenti
        existing_usernames (set, optional): Set di username già esistenti

    Returns:
        list: Lista di suggerimenti username

    Examples:
        >>> genera_username_suggerimenti("mario", {"mario", "mario1"})
        ["mario2", "mario3", "mario_2024", "mario_user"]

    References:
        [8] - Username suggestion algorithms
    """
    if not base_name:
        return []

    existing_usernames = existing_usernames or set()
    suggestions = []
    base_clean = re.sub(r'[^\w]', '', base_name.lower())

    # Suggerimenti numerici
    for i in range(2, 100):
        suggestion = f"{base_clean}{i}"
        if suggestion not in existing_usernames:
            suggestions.append(suggestion)
            if len(suggestions) >= 3:
                break

    # Suggerimenti con suffissi
    import datetime
    year = datetime.datetime.now().year
    suffixes = [f"_{year}", "_user", "_gamer", "_player"]

    for suffix in suffixes:
        suggestion = f"{base_clean}{suffix}"
        if suggestion not in existing_usernames and suggestion not in suggestions:
            suggestions.append(suggestion)

    return suggestions[:5]  # Massimo 5 suggerimenti

# =============================================================================
# CONSTANTS - Configurazioni per validazioni
# =============================================================================

class ValidationConfig:
    """
    Configurazioni per le validazioni dell'autenticazione.

    Centralizza tutti i parametri per facile manutenzione.

    References:
        [9] - Configuration management patterns
    """

    # Email validation
    EMAIL_MAX_LENGTH = 254  # RFC 5321 standard
    EMAIL_MIN_LENGTH = 5    # a@b.c

    # Username validation
    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 50
    USERNAME_PATTERN = r'^[\w\-]+$'

    # Password validation (base)
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 128

    # Input sanitization
    INPUT_MAX_LENGTH = 1000

    # Credits validation
    CREDITS_MIN_AMOUNT = 1
    CREDITS_MAX_AMOUNT = 10000
    CREDITS_DEFAULT_AMOUNT = 100

# =============================================================================
# REFERENCES / DOCUMENTAZIONE
# =============================================================================
"""
[1] Python Regex Email Validation: https://docs.python.org/3/library/re.html
[2] Werkzeug Password Hashing: https://werkzeug.palletsprojects.com/en/latest/utils/#werkzeug.security.generate_password_hash
[3] Password Hashing Best Practices: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
[4] Username Validation Standards: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
[5] Input Sanitization Security: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
[6] Basic Password Requirements: https://pages.nist.gov/800-63-3/sp800-63b.html
[7] User Experience Error Messages: https://material.io/design/patterns/errors.html
[8] Username Generation Algorithms: https://stackoverflow.com/questions/username-generation
[9] Configuration Management: https://12factor.net/config
"""