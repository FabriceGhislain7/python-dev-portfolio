from gioco.personaggio import Personaggio  # [1]
from gioco.classi import Mago, Guerriero, Ladro  # [2]
from typing import Dict, Union, Optional  # [3]
import logging

# Setup logger per transazioni crediti
credits_logger = logging.getLogger('credits')
credits_logger.setLevel(logging.INFO)

class CreditsManager:
    """
    Gestore centralizzato per tutte le operazioni sui crediti del gioco.

    Gestisce:
    - Costi creazione personaggi
    - Rimborsi cancellazione personaggi
    - Validazioni e controlli
    - Logging transazioni

    References:
        [4] - Game economy design patterns
        [5] - Virtual currency best practices
    """

    # Configurazione costi per classe (centralizzata e modificabile)
    COSTS_CONFIG = {
        "Mago": {
            "create": 20,
            "refund": 20,
            "description": "Classe magica base - costo standard"
        },
        "Guerriero": {
            "create": 25,
            "refund": 25,
            "description": "Classe fisica resistente - costo medio"
        },
        "Ladro": {
            "create": 50,
            "refund": 50,
            "description": "Classe agile avanzata - costo premium"
        }
    }

    @staticmethod
    def get_character_classes() -> Dict[str, Dict]:
        """
        Restituisce la configurazione completa delle classi e costi.

        Returns:
            Dict: Configurazione costi per tutte le classi

        References:
            [6] - Configuration management patterns
        """
        return CreditsManager.COSTS_CONFIG.copy()

    @staticmethod
    def is_valid_class(class_name: str) -> bool:
        """
        Verifica se una classe di personaggio è valida e supportata.

        Args:
            class_name (str): Nome della classe da verificare

        Returns:
            bool: True se la classe è valida, False altrimenti

        References:
            [7] - Input validation best practices
        """
        return class_name in CreditsManager.COSTS_CONFIG

    @staticmethod
    def credits_to_create(personaggio: Personaggio) -> int:
        """
        Calcola il numero di crediti necessari per creare un personaggio.

        Costi per classe:
        - Mago: 20 crediti (classe base magica)
        - Guerriero: 25 crediti (classe fisica resistente)
        - Ladro: 50 crediti (classe agile premium)

        Args:
            personaggio (Personaggio): Istanza del personaggio da creare

        Returns:
            int: Crediti necessari per la creazione

        Raises:
            ValueError: Se la classe del personaggio non è riconosciuta
            TypeError: Se l'input non è un oggetto Personaggio valido

        Examples:
            >>> mago = Mago(nome="Gandalf")
            >>> CreditsManager.credits_to_create(mago)
            20

        References:
            [8] - Game character creation economics
            [9] - Class balance and pricing
        """
        # Validazione input
        if not isinstance(personaggio, Personaggio):
            raise TypeError(f"Expected Personaggio object, got {type(personaggio)}")

        if not hasattr(personaggio, '__class__'):
            raise ValueError("Personaggio object missing class information")

        classe = personaggio.__class__.__name__

        # Controllo classe valida
        if not CreditsManager.is_valid_class(classe):
            available_classes = list(CreditsManager.COSTS_CONFIG.keys())
            raise ValueError(
                f"Classe '{classe}' del personaggio '{getattr(personaggio, 'nome', 'Unknown')}' "
                f"non riconosciuta. Classi disponibili: {available_classes}"
            )

        cost = CreditsManager.COSTS_CONFIG[classe]["create"]

        # Logging transazione
        credits_logger.info(
            f"Richiesta costo creazione: {classe} '{getattr(personaggio, 'nome', 'Unknown')}' = {cost} crediti"
        )

        return cost

    @staticmethod
    def credits_to_refund(personaggio: Personaggio) -> int:
        """
        Calcola il numero di crediti da rimborsare per la cancellazione di un personaggio.

        Rimborsi per classe:
        - Mago: 20 crediti (rimborso completo)
        - Guerriero: 25 crediti (rimborso completo)
        - Ladro: 50 crediti (rimborso completo)

        Note: Attualmente il rimborso è al 100%, ma potrebbe essere modificato
        per implementare penalità di cancellazione in futuro.

        Args:
            personaggio (Personaggio): Istanza del personaggio da cancellare

        Returns:
            int: Crediti da rimborsare all'utente

        Raises:
            ValueError: Se la classe del personaggio non è riconosciuta
            TypeError: Se l'input non è un oggetto Personaggio valido

        Examples:
            >>> ladro = Ladro(nome="Robin")
            >>> CreditsManager.credits_to_refund(ladro)
            50

        References:
            [10] - Virtual currency refund policies
            [11] - Player retention through fair refunds
        """
        # Validazione input (riuso della logica)
        if not isinstance(personaggio, Personaggio):
            raise TypeError(f"Expected Personaggio object, got {type(personaggio)}")

        if not hasattr(personaggio, '__class__'):
            raise ValueError("Personaggio object missing class information")

        classe = personaggio.__class__.__name__

        # Controllo classe valida
        if not CreditsManager.is_valid_class(classe):
            available_classes = list(CreditsManager.COSTS_CONFIG.keys())
            raise ValueError(
                f"Classe '{classe}' del personaggio '{getattr(personaggio, 'nome', 'Unknown')}' "
                f"non riconosciuta. Classi disponibili: {available_classes}"
            )

        refund = CreditsManager.COSTS_CONFIG[classe]["refund"]

        # Logging transazione
        credits_logger.info(
            f"Richiesta rimborso cancellazione: {classe} '{getattr(personaggio, 'nome', 'Unknown')}' = {refund} crediti"
        )

        return refund

    @staticmethod
    def get_class_info(class_name: str) -> Optional[Dict]:
        """
        Ottiene informazioni complete su una classe di personaggio.

        Args:
            class_name (str): Nome della classe

        Returns:
            Dict: Informazioni complete sulla classe (costi, descrizione)
            None: Se la classe non esiste

        Examples:
            >>> CreditsManager.get_class_info("Mago")
            {
                'create': 20,
                'refund': 20,
                'description': 'Classe magica base - costo standard'
            }

        References:
            [12] - Game class information systems
        """
        return CreditsManager.COSTS_CONFIG.get(class_name)

    @staticmethod
    def validate_user_credits(user_credits: float, required_credits: int) -> bool:
        """
        Verifica se un utente ha crediti sufficienti per un'operazione.

        Args:
            user_credits (float): Crediti attuali dell'utente
            required_credits (int): Crediti richiesti per l'operazione

        Returns:
            bool: True se l'utente ha crediti sufficienti

        Examples:
            >>> CreditsManager.validate_user_credits(100.0, 20)
            True
            >>> CreditsManager.validate_user_credits(10.0, 20)
            False

        References:
            [13] - Payment validation patterns
        """
        return user_credits >= required_credits

    @staticmethod
    def calculate_total_cost(personaggi: list[Personaggio]) -> int:
        """
        Calcola il costo totale per creare una lista di personaggi.

        Utile per operazioni batch o pacchetti di personaggi.

        Args:
            personaggi (list): Lista di oggetti Personaggio

        Returns:
            int: Costo totale in crediti

        Raises:
            ValueError: Se uno dei personaggi ha classe non valida

        Examples:
            >>> mago = Mago(nome="Gandalf")
            >>> guerriero = Guerriero(nome="Conan")
            >>> CreditsManager.calculate_total_cost([mago, guerriero])
            45

        References:
            [14] - Batch operations in game economies
        """
        total_cost = 0
        breakdown = []

        for personaggio in personaggi:
            cost = CreditsManager.credits_to_create(personaggio)
            total_cost += cost
            breakdown.append({
                'name': getattr(personaggio, 'nome', 'Unknown'),
                'class': personaggio.__class__.__name__,
                'cost': cost
            })

        # Logging dettagliato per operazioni batch
        credits_logger.info(f"Calcolo costo batch: {len(personaggi)} personaggi, totale: {total_cost} crediti")
        credits_logger.debug(f"Dettaglio costi: {breakdown}")

        return total_cost

    @staticmethod
    def get_cheapest_class() -> tuple[str, int]:
        """
        Trova la classe di personaggio meno costosa.

        Returns:
            tuple: (nome_classe, costo) della classe più economica

        References:
            [15] - Game balance and accessibility
        """
        cheapest = min(
            CreditsManager.COSTS_CONFIG.items(),
            key=lambda x: x[1]["create"]
        )
        return cheapest[0], cheapest[1]["create"]

    @staticmethod
    def get_most_expensive_class() -> tuple[str, int]:
        """
        Trova la classe di personaggio più costosa.

        Returns:
            tuple: (nome_classe, costo) della classe più costosa

        References:
            [15] - Game balance and accessibility
        """
        expensive = max(
            CreditsManager.COSTS_CONFIG.items(),
            key=lambda x: x[1]["create"]
        )
        return expensive[0], expensive[1]["create"]

# Backwards compatibility - mantieni le funzioni originali come wrapper
@staticmethod
def credits_to_create(personaggio: Personaggio) -> int:
    """
    Wrapper per backwards compatibility.

    References:
        [16] - API backwards compatibility
    """
    return CreditsManager.credits_to_create(personaggio)

@staticmethod
def credits_to_refund(personaggio: Personaggio) -> int:
    """
    Wrapper per backwards compatibility.

    References:
        [16] - API backwards compatibility
    """
    return CreditsManager.credits_to_refund(personaggio)

# =============================================================================
# REFERENCES / DOCUMENTAZIONE
# =============================================================================
"""
[1] Personaggio Base Class: ../gioco/personaggio.py
[2] Character Classes: ../gioco/classi.py
[3] Python Type Hints: https://docs.python.org/3/library/typing.html
[4] Game Economy Design: https://www.gamedeveloper.com/design/game-economy-design-best-practices
[5] Virtual Currency Systems: https://en.wikipedia.org/wiki/Virtual_currency
[6] Configuration Management: https://12factor.net/config
[7] Input Validation: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
[8] Character Creation Economics: https://www.gdcvault.com/play/1015883/Balancing-MMO
[9] Game Class Balance: https://www.gamedeveloper.com/design/balancing-multiplayer-games
[10] Refund Policy Design: https://www.freemium.org/blog/refund-policies/
[11] Player Retention: https://www.gamesindustry.biz/articles/2019-06-27-retention-strategies
[12] Game Information Systems: https://en.wikipedia.org/wiki/Game_design_document
[13] Payment Validation: https://stripe.com/docs/payments/payment-methods/overview
[14] Batch Operations: https://martinfowler.com/articles/patterns-of-distributed-systems/request-batch.html
[15] Game Balance Theory: https://www.designer-notes.com/?p=369
[16] API Backwards Compatibility: https://nordicapis.com/what-is-api-versioning/
"""