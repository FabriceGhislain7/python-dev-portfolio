import random, uuid, logging
from gioco.personaggio import Personaggio

from dataclasses import dataclass, field
from marshmallow import Schema, fields, post_load

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@dataclass
class Mago(Personaggio):
    """
    Classe che rappresenta un personaggio mago.
    Estende la classe personaggio con attacco diminuito e recupero
    di salute personalizzato
    """
    salute_max: int = 80
    salute: int = salute_max
    attacco_min: int = 0
    attacco_max: int = 90


    def attacca(self, mod_ambiente: int = 0) -> None:
        """
        Il Mago ha attacco minimo diminuito di 5 e attacco massimo
        aumentato di 10

        Args:
            bersaglio (Personaggio): personaggio che subisce l'attacco
            mod_ambiente (int): modificatore ambientale di attacco (default: 0)

        Returns:
            int: danno inflitto all'avversario
        """
        danno = random.randint(self.attacco_min, self.attacco_max)
        danno += mod_ambiente
        msg = f"{self.nome} lancia un incantesimo infliggendo {danno} danni!"
        logger.info(msg)
        return danno

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        """
        Recupera la salute del Mago alla fine di ogni duello del 20%

        Args:
            mod_ambiente (int): modificatore ambientale di recupero
            (default: 0)

        Returns:
            None
        """
        recupero = int((self.salute + mod_ambiente) * 0.2)
        nuova_salute = min(self.salute + recupero, 80)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"{self.nome} medita e recupera {effettivo} HP." \
            f" Salute attuale: {self.salute}"
        logger.info(msg)


@dataclass
class Guerriero(Personaggio):
    """
    Classe che rappresenta un personaggio guerriero.
    Estende la classe Personaggio, con salute_max di 120, attacco piu potente e
    guarigione post duello fissa di 30 salute
    """

    salute_max: int = 130
    salute: int = salute_max
    attacco_min: int = 20
    attacco_max: int = 100

    def attacca(self, mod_ambiente: int = 0) -> int:
        """
        Il Guerriero ha un attacco minimo aumentato di 15*  e un attacco
        massimo aumentato di 20* + il modificatore dell'ambiente corrente
        * rispetto ai campi della classe Personaggio

        Args:
            bersaglio (Personaggio): personaggio che subisce l'attacco
            mod_ambiente (int): modificatore ambientale di attacco (default: 0)

        Returns:
            None
        """
        danno = random.randint(
            self.attacco_min,
            self.attacco_max + mod_ambiente
        )
        msg = f"{self.nome} colpisce con la spada infliggendo {danno} danni!"
        logger.info(msg)
        return danno

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        """
        Il guerriero al termine di ogni duello recupera salute pari 30

        Args:
            mod_ambiente (int): modificatore ambientale di recupero
            (default: 0)

        Returns:
            None
        """
        recupero = 30 + mod_ambiente
        nuova_salute = min(self.salute + recupero, 120)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"{self.nome} si fascia le ferite e recupera {effettivo} HP." \
            f" Salute attuale: {self.salute}"
        logger.info(msg)


@dataclass
class Ladro(Personaggio):
    """
    Estende la classe Personaggio, ha salute elevata a 140, +5 attacco_max e
    attacco_min, recupera punti salute al termine del duello
    casualmente in un range 10-40
    """
    salute_max: int = 120
    salute: int = salute_max
    attacco_max: int = 85
    attacco_min: int = 10


    def attacca(self, mod_ambiente: int = 0) -> int:
        """
        attacco del ladro valore random tra attacco_min e attacco_max
        con un modificatore ambientale, se l'azione ha successo

        Args:
            mod_ambiente (int): modificatore ambientale di attacco (default: 0)

        Returns:
            danno (int): danno inflitto all'avversario
        """
        danno = 0
        if self.esegui_azione():
            danno = random.randint(
                self.attacco_min, self.attacco_max
            ) + mod_ambiente
            msg = f"{self.nome} colpisce furtivamente infliggendo {danno} danni!"
        else:
            msg = f"{self.nome} tenta di attaccare ma fallisce!"
        logger.info(msg)
        return danno

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        """
        Permette al ladro di recuperare un numero casuale
        di punti salute in un range 10-40, modificato dall'ambiente

        Args:
            mod_ambiente (int): modificatore ambientale di recupero
            (default: 0)

        Returns:
            None
        """
        recupero = random.randint(10, 40) + mod_ambiente
        nuova_salute = min(self.salute + recupero, 140)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"{self.nome} si cura rapidamente e recupera {effettivo} HP. " \
            f"Salute attuale: {self.salute}"
        logger.info(msg)


class PersonaggioSchema(Schema):
    """
    Schema per la serializzazione/deserializzazione dei personaggi.
    Utilizza Marshmallow per definire i campi e le loro proprietà.
    """
    classe = fields.String(required=True)
    id = fields.UUID(load_default=lambda: uuid.uuid4())

    storico_danni_subiti = fields.List(fields.Integer(), load_default=list)

    def _set_default_if_empty(self, data, key, default):
        """
        Imposta un valore di default per il campo 'key' se il campo è assente o vuoto.
        """
        if key not in data or data[key] in (None, '', [], {}):
            data[key] = default

    @post_load
    def make_personaggio(self, data, **kwargs):
        print(f"\nimport: \n{data}\n")
        classe = data.get("classe", "Personaggio")
        # Rimuovi il campo 'classe' dai dati prima di creare l'istanza
        data_clean = {k: v for k, v in data.items() if k != "classe"}

        if classe == "Mago":
            # Applica i default specifici del Mago se i campi sono assenti o vuoti
            self._set_default_if_empty(data_clean, "salute_max", 80)
            self._set_default_if_empty(data_clean, "salute", 80)
            self._set_default_if_empty(data_clean, "attacco_min", 0)
            self._set_default_if_empty(data_clean, "attacco_max", 90)
            char = Mago(**data_clean)
            char.classe = classe
            return char
        elif classe == "Guerriero":
            # Applica i default specifici del Guerriero se i campi sono assenti o vuoti
            self._set_default_if_empty(data_clean, "salute_max", 120)
            self._set_default_if_empty(data_clean, "salute", 120)
            self._set_default_if_empty(data_clean, "attacco_min", 20)
            self._set_default_if_empty(data_clean, "attacco_max", 100)
            char = Guerriero(**data_clean)
            char.classe = classe
            return char
        elif classe == "Ladro":
            # Applica i default specifici del Ladro se i campi sono assenti o vuoti
            self._set_default_if_empty(data_clean, "salute_max", 100)
            self._set_default_if_empty(data_clean, "salute", 100)
            self._set_default_if_empty(data_clean, "attacco_min", 10)
            self._set_default_if_empty(data_clean, "attacco_max", 85)
            char = Ladro(**data_clean)
            char.classe = classe
            return char
        else:
            # Applica i default generici del Personaggio se i campi sono assenti o vuoti
            self._set_default_if_empty(data_clean, "salute_max", 200)
            self._set_default_if_empty(data_clean, "salute", 100)
            self._set_default_if_empty(data_clean, "attacco_min", 5)
            self._set_default_if_empty(data_clean, "attacco_max", 80)
            return Personaggio(**data_clean)
