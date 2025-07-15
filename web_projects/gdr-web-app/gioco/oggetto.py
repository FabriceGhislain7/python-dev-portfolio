from dataclasses import dataclass, field
import uuid


@dataclass
class Oggetto:
    """
    Inizializza un oggetto con nome e tipo

    Args:
        nome (str): Nome dell'oggetto

    Returns:
        None

    """
    nome: str
    usato: bool = False
    valore: int = 30
    tipo_oggetto: str = ""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    classe: str = field(init=False)

    def __post_init__(self):
        """
        Imposta automaticamente il nome della classe se non è già impostato
        """
        if not hasattr(self, 'classe') or not self.classe:
            self.classe = self.__class__.__name__

    def usa(
            self,
            mod_ambiente: int = 0
            ) -> int:
        """
        Metodo da implementare in ogni oggetto

        Args:
            mod_ambiente (int): variabile dell'Ambiente in cui si trova
            l'oggetto

        Returns:
            int: Valore dell'oggetto usato
        """
        raise NotImplementedError("Questo oggetto non ha effetto definito.")


@dataclass
class PozioneCura(Oggetto):
    """
    Cura il personaggio che la usa di un certo valore
    """
    nome: str = "Pozione Rossa"
    valore: int = 30
    classe: str = "PozioneCura"
    tipo_oggetto: str = "Ristorativo"

    def usa(self, mod_ambiente: int = 0) -> int:
        """
        Cura il personaggio che la usa di un certo valore

        Args:
            mod_ambiente (int): variabile dell'Ambiente in cui si trova
            l'oggetto

        Returns:
            int: Valore di cura della pozione
        """
        self.usato = True
        cura = self.valore + mod_ambiente
        return cura


@dataclass
class BombaAcida(Oggetto):
    """
    Infligge danno pari al valore(Proprietà)
    """
    nome: str = "Bomba Acida"
    valore: int = 30
    classe: str = "BombaAcida"
    tipo_oggetto: str = "Offensivo"

    def usa(self, mod_ambiente: int = 0) -> int:
        """
        Infligge danno al bersaglio
        !!!ATTENZIONE!!!
        Il valore viene passato come un valore negativo!

        Args:
            mod_ambiente (int): variabile dell'Ambiente in cui si trova
            l'oggetto

        Returns:
            int: Danno inflitto dalla bomba
        """
        self.usato = True
        danno = - (self.valore + mod_ambiente)
        return danno


@dataclass
class Medaglione(Oggetto):
    """
    Incrementa l'attacco_max del personaggio che lo usa
    """
    nome: str = "Medaglione"
    valore: int = 10
    tipo_oggetto: str = "Buff"
    classe: str = "Medaglione"

    def usa(self, mod_ambiente: int = 0) -> None:
        """
        Incrementa l'attacco_max del personaggio che lo usa

        Args:
            mod_ambiente (int): variabile dell'Ambiente in cui si trova
            l'oggetto

        Returns:
            None
        """

        self.usato = True
        mod = int(self.valore + mod_ambiente)
        return mod