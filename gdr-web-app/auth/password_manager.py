import re
import secrets
import string
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

# Setup logger per password security
password_logger = logging.getLogger('password_security')
password_logger.setLevel(logging.INFO)

class PasswordStrength(Enum):
    """
    Enumerazione per i livelli di sicurezza delle password.

    References:
        [1] - Password strength classification standards
    """
    VERY_WEAK = 1
    WEAK = 2
    MEDIUM = 3
    STRONG = 4
    VERY_STRONG = 5

@dataclass
class PasswordValidationResult:
    """
    Risultato della validazione di una password.

    Attributes:
        is_valid (bool): Se la password è valida
        strength (PasswordStrength): Livello di sicurezza
        score (int): Punteggio 0-100
        issues (List[str]): Lista dei problemi trovati
        suggestions (List[str]): Suggerimenti per migliorare

    References:
        [2] - Password validation response patterns
    """
    is_valid: bool
    strength: PasswordStrength
    score: int
    issues: List[str]
    suggestions: List[str]

class PasswordManager:
    """
    Gestore completo per validazione, generazione e analisi password sicure.

    Features:
    - Validazione con criteri personalizzabili
    - Generazione password sicure
    - Analisi forza password
    - Controllo password comuni/compromesse
    - Suggerimenti miglioramento

    References:
        [3] - NIST Password Guidelines
        [4] - OWASP Authentication Cheat Sheet
    """

    # Configurazione criteri password
    DEFAULT_CONFIG = {
        'min_length': 8,
        'max_length': 128,
        'require_uppercase': True,
        'require_lowercase': True,
        'require_digits': True,
        'require_special_chars': True,
        'min_special_chars': 1,
        'forbid_common_patterns': True,
        'forbid_personal_info': True,
        'max_repeated_chars': 2
    }

    # Caratteri speciali consigliati (evitando quelli problematici in alcuni sistemi)
    SAFE_SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Pattern comuni da evitare
    COMMON_PATTERNS = [
        r'123456',
        r'password',
        r'qwerty',
        r'abc123',
        r'admin',
        r'letmein',
        r'welcome',
        r'monkey',
        r'dragon',
        r'master'
    ]

    # Sequenze da evitare
    SEQUENTIAL_PATTERNS = [
        r'abcd',
        r'1234',
        r'qwer',
        r'asdf'
    ]

    def __init__(self, config: Optional[Dict] = None):
        """
        Inizializza il gestore password con configurazione personalizzata.

        Args:
            config (Dict, optional): Configurazione personalizzata

        References:
            [5] - Configurable security policies
        """
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        password_logger.info("PasswordManager inizializzato con configurazione personalizzata")

    def validate_password(self, password: str, user_info: Optional[Dict] = None) -> PasswordValidationResult:
        """
        Valida una password secondo tutti i criteri di sicurezza.

        Args:
            password (str): Password da validare
            user_info (Dict, optional): Info utente per controlli personalizzazione
                Esempio: {'username': 'mario', 'email': 'mario@email.com', 'name': 'Mario Rossi'}

        Returns:
            PasswordValidationResult: Risultato completo della validazione

        Examples:
            >>> pm = PasswordManager()
            >>> result = pm.validate_password("MySecure123!")
            >>> print(f"Valid: {result.is_valid}, Strength: {result.strength}")

        References:
            [6] - Comprehensive password validation
        """
        issues = []
        suggestions = []
        score = 0

        # Validazione lunghezza
        if len(password) < self.config['min_length']:
            issues.append(f"Password troppo corta (minimo {self.config['min_length']} caratteri)")
            suggestions.append(f"Aumenta la lunghezza ad almeno {self.config['min_length']} caratteri")
        else:
            score += min(20, len(password) - self.config['min_length'] + 10)

        if len(password) > self.config['max_length']:
            issues.append(f"Password troppo lunga (massimo {self.config['max_length']} caratteri)")

        # Controllo caratteri richiesti
        if self.config['require_uppercase'] and not re.search(r'[A-Z]', password):
            issues.append("Manca almeno una lettera maiuscola")
            suggestions.append("Aggiungi almeno una lettera maiuscola (A-Z)")
        elif re.search(r'[A-Z]', password):
            score += 15

        if self.config['require_lowercase'] and not re.search(r'[a-z]', password):
            issues.append("Manca almeno una lettera minuscola")
            suggestions.append("Aggiungi almeno una lettera minuscola (a-z)")
        elif re.search(r'[a-z]', password):
            score += 15

        if self.config['require_digits'] and not re.search(r'\d', password):
            issues.append("Manca almeno un numero")
            suggestions.append("Aggiungi almeno un numero (0-9)")
        elif re.search(r'\d', password):
            score += 15

        if self.config['require_special_chars'] and not re.search(f'[{re.escape(self.SAFE_SPECIAL_CHARS)}]', password):
            issues.append("Manca almeno un carattere speciale")
            suggestions.append(f"Aggiungi almeno un carattere speciale ({self.SAFE_SPECIAL_CHARS[:10]}...)")
        elif re.search(f'[{re.escape(self.SAFE_SPECIAL_CHARS)}]', password):
            score += 15

        # Controllo caratteri ripetuti
        if self.config['max_repeated_chars'] > 0:
            repeated = self._find_repeated_chars(password)
            if repeated and len(repeated) > self.config['max_repeated_chars']:
                issues.append(f"Troppi caratteri ripetuti consecutivi: '{repeated}'")
                suggestions.append("Evita di ripetere lo stesso carattere più volte consecutive")
                score -= 10

        # Controllo pattern comuni
        if self.config['forbid_common_patterns']:
            common_found = self._check_common_patterns(password.lower())
            if common_found:
                issues.append(f"Contiene pattern comuni: {', '.join(common_found)}")
                suggestions.append("Evita parole comuni come 'password', '123456', ecc.")
                score -= 20

        # Controllo informazioni personali
        if self.config['forbid_personal_info'] and user_info:
            personal_found = self._check_personal_info(password.lower(), user_info)
            if personal_found:
                issues.append(f"Contiene informazioni personali: {', '.join(personal_found)}")
                suggestions.append("Non usare nome utente, email o dati personali nella password")
                score -= 15

        # Controllo diversità caratteri
        char_diversity = self._calculate_character_diversity(password)
        score += char_diversity

        # Bonus per lunghezza extra
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 5

        # Determina livello di sicurezza
        score = max(0, min(100, score))
        strength = self._calculate_strength(score, len(issues))
        is_valid = len(issues) == 0

        # Logging
        password_logger.info(f"Password validata: valid={is_valid}, strength={strength.name}, score={score}")

        return PasswordValidationResult(
            is_valid=is_valid,
            strength=strength,
            score=score,
            issues=issues,
            suggestions=suggestions
        )

    def generate_secure_password(
        self, 
        length: int = 12, 
        include_symbols: bool = True,
        readable: bool = False,
        custom_requirements: Optional[Dict] = None
    ) -> str:
        """
        Genera una password sicura con criteri personalizzabili.

        Args:
            length (int): Lunghezza password (default: 12)
            include_symbols (bool): Include caratteri speciali (default: True)
            readable (bool): Genera password più leggibile (evita caratteri ambigui)
            custom_requirements (Dict): Requisiti personalizzati

        Returns:
            str: Password sicura generata

        Examples:
            >>> pm = PasswordManager()
            >>> password = pm.generate_secure_password(16, readable=True)
            >>> print(f"Generated: {password}")

        References:
            [7] - Secure random password generation
            [8] - Cryptographically secure randomness
        """
        if length < 4:
            raise ValueError("Lunghezza minima password: 4 caratteri")

        # Definisci set di caratteri
        if readable:
            # Caratteri più leggibili (evita 0/O, 1/l/I, ecc.)
            lowercase = 'abcdefghijkmnopqrstuvwxyz'  # no l
            uppercase = 'ABCDEFGHJKLMNPQRSTUVWXYZ'   # no I, O
            digits = '23456789'                       # no 0, 1
            symbols = '!@#$%^&*+-='                  # simboli semplici
        else:
            # Set completo
            lowercase = string.ascii_lowercase
            uppercase = string.ascii_uppercase
            digits = string.digits
            symbols = self.SAFE_SPECIAL_CHARS

        # Costruisci pool caratteri
        char_pool = lowercase + uppercase + digits
        if include_symbols:
            char_pool += symbols

        # Assicura almeno un carattere per tipo richiesto
        required_chars = []
        if self.config['require_lowercase']:
            required_chars.append(secrets.choice(lowercase))
        if self.config['require_uppercase']:
            required_chars.append(secrets.choice(uppercase))
        if self.config['require_digits']:
            required_chars.append(secrets.choice(digits))
        if self.config['require_special_chars'] and include_symbols:
            required_chars.append(secrets.choice(symbols))

        # Genera resto della password
        remaining_length = length - len(required_chars)
        remaining_chars = [secrets.choice(char_pool) for _ in range(remaining_length)]

        # Combina e mescola
        all_chars = required_chars + remaining_chars
        password_list = list(all_chars)

        # Mescola usando secrets (cryptographically secure)
        for i in range(len(password_list)):
            j = secrets.randbelow(len(password_list))
            password_list[i], password_list[j] = password_list[j], password_list[i]

        password = ''.join(password_list)

        # Logging (senza mostrare la password)
        password_logger.info(f"Password generata: length={length}, symbols={include_symbols}, readable={readable}")

        return password

    def suggest_password_improvements(self, password: str) -> List[str]:
        """
        Suggerisce miglioramenti specifici per una password.

        Args:
            password (str): Password da analizzare

        Returns:
            List[str]: Lista di suggerimenti specifici

        References:
            [9] - User-friendly security guidance
        """
        validation = self.validate_password(password)

        if validation.is_valid:
            return ["Password già sicura! 🎉"]

        improvements = validation.suggestions.copy()

        # Suggerimenti aggiuntivi basati sull'analisi
        if validation.score < 30:
            improvements.append("💡 Prova il generatore automatico per una password più sicura")

        if len(password) < 10:
            improvements.append("🔒 Password più lunghe sono più sicure - prova almeno 12 caratteri")

        return improvements

    def generate_password_suggestions(self, count: int = 3, length: int = 12) -> List[Dict]:
        """
        Genera multiple opzioni di password sicure con informazioni.

        Args:
            count (int): Numero di password da generare
            length (int): Lunghezza delle password

        Returns:
            List[Dict]: Lista di password con info (password, strength, score)

        Examples:
            >>> pm = PasswordManager()
            >>> suggestions = pm.generate_password_suggestions(3)
            >>> for s in suggestions:
            ...     print(f"{s['password']} - Strength: {s['strength']}")

        References:
            [10] - Multiple secure options for users
        """
        suggestions = []

        for i in range(count):
            # Varia le caratteristiche per diversità
            readable = i % 2 == 0  # Alterna readable/non-readable
            password = self.generate_secure_password(
                length=length + (i % 3),  # Varia lunghezza leggermente
                readable=readable
            )

            validation = self.validate_password(password)

            suggestions.append({
                'password': password,
                'strength': validation.strength,
                'score': validation.score,
                'readable': readable,
                'description': self._get_password_description(validation.strength)
            })

        # Ordina per score (migliori prima)
        suggestions.sort(key=lambda x: x['score'], reverse=True)

        password_logger.info(f"Generate {count} password suggestions")
        return suggestions

    def check_password_strength_realtime(self, password: str) -> Dict:
        """
        Controllo in tempo reale per UI interattive (form con feedback live).

        Args:
            password (str): Password parziale da controllare

        Returns:
            Dict: Info per UI (score, color, message, progress)

        References:
            [11] - Real-time password feedback UX
        """
        if not password:
            return {
                'score': 0,
                'color': 'gray',
                'message': 'Inserisci una password',
                'progress': 0,
                'class': 'password-empty'
            }

        validation = self.validate_password(password)

        # Mapping per UI
        ui_mapping = {
            PasswordStrength.VERY_WEAK: {
                'color': 'red',
                'message': 'Molto debole - Non sicura',
                'class': 'password-very-weak'
            },
            PasswordStrength.WEAK: {
                'color': 'orange',
                'message': 'Debole - Aggiungi più caratteri',
                'class': 'password-weak'
            },
            PasswordStrength.MEDIUM: {
                'color': 'yellow',
                'message': 'Media - Quasi buona',
                'class': 'password-medium'
            },
            PasswordStrength.STRONG: {
                'color': 'lightgreen',
                'message': 'Forte - Buona sicurezza',
                'class': 'password-strong'
            },
            PasswordStrength.VERY_STRONG: {
                'color': 'green',
                'message': 'Molto forte - Eccellente!',
                'class': 'password-very-strong'
            }
        }

        ui_info = ui_mapping[validation.strength]

        return {
            'score': validation.score,
            'progress': validation.score,
            'is_valid': validation.is_valid,
            'issues_count': len(validation.issues),
            'suggestions_count': len(validation.suggestions),
            **ui_info
        }

    # Metodi helper privati
    def _find_repeated_chars(self, password: str) -> Optional[str]:
        """Trova sequenze di caratteri ripetuti."""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                # Trova tutta la sequenza ripetuta
                j = i + 3
                while j < len(password) and password[j] == password[i]:
                    j += 1
                return password[i:j]
        return None

    def _check_common_patterns(self, password: str) -> List[str]:
        """Controlla pattern comuni nella password."""
        found_patterns = []

        for pattern in self.COMMON_PATTERNS:
            if re.search(pattern, password):
                found_patterns.append(pattern)

        for pattern in self.SEQUENTIAL_PATTERNS:
            if pattern in password or pattern[::-1] in password:  # anche al contrario
                found_patterns.append(pattern)

        return found_patterns

    def _check_personal_info(self, password: str, user_info: Dict) -> List[str]:
        """Controlla se la password contiene info personali."""
        found_info = []

        checks = {
            'username': user_info.get('username', ''),
            'email_prefix': user_info.get('email', '').split('@')[0] if user_info.get('email') else '',
            'name': user_info.get('name', ''),
            'first_name': user_info.get('first_name', ''),
            'last_name': user_info.get('last_name', '')
        }

        for info_type, info_value in checks.items():
            if info_value and len(info_value) >= 3 and info_value.lower() in password:
                found_info.append(info_type)

        return found_info

    def _calculate_character_diversity(self, password: str) -> int:
        """Calcola bonus per diversità caratteri."""
        unique_chars = len(set(password))
        total_chars = len(password)

        if total_chars == 0:
            return 0

        diversity_ratio = unique_chars / total_chars
        return int(diversity_ratio * 20)  # Max 20 punti per diversità

    def _calculate_strength(self, score: int, issues_count: int) -> PasswordStrength:
        """Determina il livello di sicurezza basato su score e problemi."""
        if issues_count > 0:
            if score < 30:
                return PasswordStrength.VERY_WEAK
            elif score < 50:
                return PasswordStrength.WEAK
            else:
                return PasswordStrength.MEDIUM
        else:
            if score >= 90:
                return PasswordStrength.VERY_STRONG
            elif score >= 70:
                return PasswordStrength.STRONG
            else:
                return PasswordStrength.MEDIUM

    def _get_password_description(self, strength: PasswordStrength) -> str:
        """Ottiene descrizione user-friendly della forza password."""
        descriptions = {
            PasswordStrength.VERY_WEAK: "Password molto debole - evita di usarla",
            PasswordStrength.WEAK: "Password debole - non consigliata",
            PasswordStrength.MEDIUM: "Password media - accettabile ma migliorabile", 
            PasswordStrength.STRONG: "Password forte - buona sicurezza",
            PasswordStrength.VERY_STRONG: "Password molto forte - sicurezza eccellente"
        }
        return descriptions[strength]

# =============================================================================
# UTILITY FUNCTIONS per backwards compatibility e facilità d'uso
# =============================================================================

# Istanza globale con configurazione default
_default_manager = PasswordManager()

def validate_password_simple(password: str) -> Tuple[bool, str]:
    """
    Validazione password semplificata per compatibilità.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)

    References:
        [12] - Simple validation API
    """
    result = _default_manager.validate_password(password)

    if result.is_valid:
        return True, ""
    else:
        return False, "; ".join(result.issues)

def generate_password(length: int = 12) -> str:
    """
    Generazione password semplificata.

    References:
        [13] - Simple generation API
    """
    return _default_manager.generate_secure_password(length=length)

def get_password_strength(password: str) -> str:
    """
    Ottiene forza password come stringa.

    Returns:
        str: Livello di sicurezza ('molto_debole', 'debole', ecc.)
    """
    result = _default_manager.validate_password(password)
    return result.strength.name.lower()

# =============================================================================
# REFERENCES / DOCUMENTAZIONE
# =============================================================================
"""
[1] NIST Password Guidelines: https://pages.nist.gov/800-63-3/sp800-63b.html
[2] Password Validation Patterns: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
[3] NIST Special Publication 800-63B: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63b.pdf
[4] OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
[5] Security Policy Configuration: https://csrc.nist.gov/Projects/Risk-Management/sp800-53-controls/release-search#!/control?version=5.1
[6] Password Validation Best Practices: https://auth0.com/blog/password-strength-indicators/
[7] Secure Random Generation: https://docs.python.org/3/library/secrets.html
[8] Cryptographic Randomness: https://cryptography.io/en/latest/random-numbers/
[9] UX Security Guidelines: https://material.io/design/patterns/authentication.html
[10] Password Generation Strategies: https://www.ncsc.gov.uk/blog-post/the-logic-behind-three-random-words
[11] Real-time Feedback UX: https://ux.stackexchange.com/questions/password-strength-indicators
[12] API Design Best Practices: https://restfulapi.net/
[13] Python Secrets Module: https://peps.python.org/pep-0506/
"""