import random
import logging
from typing import Dict
from dataclasses import dataclass

from marshmallow import Schema, fields, post_load
from gioco.oggetto import BombaAcida, Oggetto, PozioneCura
from gioco.classi import Guerriero, Ladro, Mago
from gioco.personaggio import Personaggio

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class Ambiente():
    """
    E responsabile alla gestione di variabili  globali dovuti all'ambiente
    interagisce con le classi Personaggio e Oggetto
    """
    nome: str
    mod_attacco: int = 0
    mod_cura: float = 0.0

    def modifica_attacco(self, attaccante: Personaggio) -> int:
        raise NotImplementedError

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        raise NotImplementedError

    def modifica_cura(self, soggetto: Personaggio) -> int:
        raise NotImplementedError

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        return {
            "classe": self.__class__.__name__,
            "nome": self.nome,
            "modifica_attacco": self.mod_attacco,
            "modifica_cura": self.mod_cura
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Ambiente':
        """ricrea il classe corretta in base al campo "classe"

        Args:
            data (dict):

        Returns:
            Ambiente:
        """
        nome = data.get("classe", "")
        return AmbienteFactory.usa_ambiente(nome)


@dataclass
class Foresta(Ambiente):
    """
    La classe Foresta eredita da Ambiente e rappresenta un ambiente specifico
    con modifiche agli attacchi dei guerrieri e alla cura a fine turno per i
    ladri.
    """
    nome: str = "Foresta"
    mod_attacco: int = 5
    mod_cura: float = 5.0

    def modifica_attacco(self, attaccante: Personaggio) -> int:
        """
        Il metodo controlla se l'attaccante è un Guerriero e, in caso
        affermativo, aumenta il suo attacco massimo di un valore definito
        modifica_attacco=5.

        Args:
            attaccante (Personaggio): Attaccante

        Returns:
            int: Il valore intero che andrà a modificare l'attacco o 0 se
            l'attaccante non è un guerriero
        """
        if isinstance(attaccante, Guerriero):
            logger.info(
                f"{attaccante.nome} guadagna {self.modifica_attacco}"
                f"attacco nella Foresta!"
            )
            return self.mod_attacco
        return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        """
        Questo metodo non modifica l'effetto dell'oggetto.

        Args:
            oggetto (Oggetto): Oggetto da modificare

        returns:
            int: 0
        """
        return 0

    def modifica_cura(self, soggetto: Personaggio) -> int:
        """
        Questa funzione aumenta la cura del ladro di un valore definito
        nell'ambiente Foresta.

        Args:
            soggetto (Personaggio): Il personaggio che riceve la cura se è un
            ladro

        returns:
            int: L'aumento della cura se il soggetto è un ladro, altrimenti 0
        """
        if isinstance(soggetto, Ladro):
            return int(self.mod_cura)
        return 0


@dataclass
class Vulcano(Ambiente):
    """
    La classe Vulcano eredita da Ambiente e rappresenta un ambiente specifico
    con modifiche agli attacchi dei maghi e dei ladri, un incremento random dei
    danni delle bombe acide e alla cura a fine turno per tutti.
    """
    nome: str = "Vulcano"
    mod_attacco: int = 10
    mod_cura: float = -5.0

    def modifica_attacco(self, attaccante: Personaggio) -> int:
        """
        Il metodo controlla se l'attaccante è un Mago e, in caso affermativo,
        aumenta il suo attacco massimo di un valore definito
        modifica_attacco=10.
        Se l'attaccante è un Ladro, diminuisce il suo attacco massimo di un
        valore definito modifica_attacco=10.

        Args:
            attaccante (Personaggio): Il personaggio che attacca

        returns:
            int: L'aumento o la diminuzione dell'attacco massimo
        """

        if isinstance(attaccante, Mago):
            logger.info(
                f"{attaccante.nome} guadagna {self.modifica_attacco}"
                "attacco nel Vulcano!"
            )
            return self.mod_attacco
        elif isinstance(attaccante, Ladro):
            logger.info(
                f"{attaccante.nome} perde {self.modifica_attacco}"
                "attacco nel Vulcano!"
            )
            return -self.mod_attacco
        return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        """
        Il metodo aumenta il danno della bomba acida di un valore casuale
        da 0 a 15

        Args:
            oggetto (Oggetto): Oggetto da modificare

        returns:
            int: Aumento del danno della bomba acida
        """
        if isinstance(oggetto, BombaAcida):
            variazione = random.randint(0, 15)
            logger.info(
                f"Nella {self.nome}, la Bomba Acida guadagna {variazione}"
                f" danni!"
            )
            return variazione
        return 0

    def modifica_cura(self, soggetto: Personaggio) -> int:
        """
        Questo metodo aumenta la cura di tutti i personaggi di un valore
        definito nell'ambiente Vulcano.

        Args:
            soggetto (Personaggio): Il personaggio che riceve la cura

        returns:
            int: L'aumento della cura se il soggetto è un ladro, altrimenti 0

        """
        return int(self.mod_cura)


@dataclass
class Palude(Ambiente):
    """
    La classe Palude eredita da Ambiente e rappresenta un ambiente specifico
    con un decremento agli attacchi dei ladri e dei guerrieri, e alle cure
    delle pozioni
    """
    nome: str = "Palude"
    mod_attacco: int = -5
    mod_cura: float = 0.3

    def modifica_attacco(self, attaccante: Personaggio) -> int:
        """
        Il metodo controlla se l'attaccante è un Guerriero o un Ladro e, in
        caso affermativo, diminuisce il suo attacco massimo di un valore
        definito modifica_attacco=-5 nell'ambiente Palude.

        Args:
            attaccante (Personaggio): Il personaggio che attacca

        returns:
            int: La diminuzione dell'attacco massimo
        """
        if isinstance(attaccante, (Guerriero, Ladro)):
            logger.info(
                f"{attaccante.nome} perde {-self.mod_attacco} "
                "attacco nella Palude!")
            return self.mod_attacco
        return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        """
        Il metodo riduce l'effetto della Pozione Cura del %30
        Args:
            oggetto (Oggetto): Oggetto da modificare

        returns:
            int: Riduzione dell'effetto della Pozione Cura
        """
        if isinstance(oggetto, PozioneCura):
            riduzione = int(oggetto.valore * self.mod_cura)
            logger.info(
                f"Nella {self.nome}, la Pozione Cura ha effetto ridotto di"
                f"{riduzione} punti!"
                )
            return -riduzione
        return 0

    def modifica_cura(self, soggetto: Personaggio) -> int:
        return 0


# ------------------------------------------
class AmbienteFactory:
    """
    Factory per la generazione di ambienti nel sistema di combattimento.
    Fornisce metodi per creare un ambiente casuale oppure selezionarlo
    manualmente.
    """
    @staticmethod
    def get_opzioni() -> Dict[str, Ambiente]:
        return {
            "1": Foresta(),
            "2": Vulcano(),
            "3": Palude()
        }

    @staticmethod
    def usa_ambiente(scelta: str) -> Ambiente:
        """
        Permette all'utente di selezionare un ambiente tra quelli disponibili.

        Se l'input è valido, viene restituito l'ambiente predefinito (Foresta).

        Args:
            None

        Returns:
            ambiente: Un'istanza della sottoclasse selezionata di Ambiente, o
            Foresta come default.
        """
        mapping = AmbienteFactory.get_opzioni()
        scelta = scelta.strip().lower()
        if scelta in mapping:
            env = mapping[scelta]
            logger.info(f"selezionato ambiente {env.nome}")
            return env
        # fallback
        logger.warning(f"scelta ambiente sconosciuta: {scelta}, uso foresta")
        return Foresta()

    @staticmethod
    def ambiente_random() -> Ambiente:
        """
        Sorteggia un ambiente casuale tra quelli disponibili.

        Args:
            None

        Returns:
            ambiente: Un'istanza di una sottoclasse di Ambiente scelta
            casualmente (Foresta, Vulcano o Palude).
        """
        random_choice = random.choice(
            list(AmbienteFactory.get_opzioni().values())
        )
        logger.info(f"Ambiente Casuale Selezionato: {random_choice}")
        return random_choice


def get_all_subclasses(cls):
    """
    Ottiene tutte le sottoclassi di una classe base, utilizzata per
    la deserializzazione dinamica tramite Marshmallow.

    Args:
        cls: La classe base di cui ottenere le sottoclassi

    Returns:
        set: Un set contenente tutte le sottoclassi
    """
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        # subclasses.update(get_all_subclasses(subclass))
        # nel caso di sottoclassi indirette
    return subclasses


class AmbienteSchema(Schema):
    classe = fields.String(required=True)
    nome = fields.String(required=True)
    mod_attacco = fields.Integer()
    mod_cura = fields.Float()

    @post_load
    def make_obj(self, data, **kwargs):
        # Crea la mappa dinamica: nome classe -> classe Python
        classe_nome = data.get("classe")
        ambienti_map = {
            subcls.__name__: subcls
            for subcls in get_all_subclasses(Ambiente)
        }

        # rimuovo classe dai dati per evitare conflitti
        data_clean = {k: v for k, v in data.items() if k != 'classe'}

        if classe_nome in ambienti_map:
            ambiente_cls = ambienti_map[classe_nome]
            return ambiente_cls(**data_clean)
        else:
            # Fallback alla classe base Ambiente
            return Ambiente(**data_clean)

    def dump(self, obj, *, many=None, **kwargs):
        """
        Override del metodo dump per aggiungere automaticamente il campo classe
        """
        # Ottieni i dati base dall'oggetto usando il metodo parent
        data = super().dump(obj, many=many, **kwargs)

        if many:
            # Se stiamo serializzando una lista di oggetti
            if isinstance(obj, (list, tuple)) and isinstance(data, list):
                for i, item_data in enumerate(data):
                    if i < len(obj) and hasattr(obj[i], '__class__'):
                        item_data['classe'] = obj[i].__class__.__name__
        else:
            # Se stiamo serializzando un singolo oggetto
            if isinstance(data, dict) and hasattr(obj, '__class__'):
                data['classe'] = obj.__class__.__name__

        return data