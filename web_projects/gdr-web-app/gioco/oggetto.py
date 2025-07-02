from gioco.personaggio import Personaggio

# Modulo oggetti
# Contiene la classe base Oggetto e le classi derivate

class Oggetto ():
    """
    Classe padre di tutti gli oggetti contenibili nell'inventario
    """
    def __init__(
        self,
        nome: str,
        valore: int = 0,
        tipo_oggetto: str = ""
        ) -> None:
        """
        Inizializza un oggetto con nome e tipo

        Args:
            nome (str): Nome dell'oggetto

        Returns:
            None

        """
        self.nome = nome
        self.usato = False
        self.valore = valore
        self.tipo_oggetto = tipo_oggetto


    def usa(
            self,
            mod_ambiente: int = 0
            ) -> int:
        """
        Metodo da implementare in ogni oggetto

        Args:
            mod_ambiente (int): variabile dell'Ambiente in cui si trova l'oggetto

        Returns:
            int: Valore dell'oggetto usato
        """
        raise NotImplementedError("Questo oggetto non ha effetto definito.")


    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        return {
            "classe": self.__class__.__name__,
            "nome": self.nome,
            "usato": self.usato,
            "valore": self.valore,
            "tipo_oggetto": self.tipo_oggetto
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Oggetto":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        oggetto = cls(nome=data["nome"])
        oggetto.usato = data.get("usato", False)
        oggetto.valore = data.get("valore", 0)
        oggetto.tipo_oggetto = data.get("tipo_oggetto", "")
        return oggetto


class PozioneCura(Oggetto):
    """
    Cura il personaggio che la usa di un certo valore
    """
    def __init__(
            self,
            nome: str = "Pozione Rossa",
            valore: int = 30,
            tipo_oggetto: str = "Ristorativo"
            ) -> None:
        """
        Inizializza una pozione di cura

        Args:
            nome (str): Nome della pozione
            valore (int): Valore di cura della pozione
            tipo_oggetto (str): Tipologia di oggetto

        Returns:
            None
        """
        super().__init__(nome=nome, valore=valore, tipo_oggetto=tipo_oggetto)

    def usa(self, mod_ambiente: int = 0) -> int:
        """
        Cura il personaggio che la usa di un certo valore

        Args:
            mod_ambiente (int): variabile dell'Ambiente in cui si trova l'oggetto

        Returns:
            int: Valore di cura della pozione
        """
        self.usato = True
        return self.valore + mod_ambiente

    def to_dict(self) -> dict:
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "PozioneCura":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        oggetto = cls(nome=data["nome"])
        oggetto.usato = data.get("usato", False)
        oggetto.valore = data.get("valore", 30)
        oggetto.tipo_oggetto = data.get("tipo_oggetto", "Ristorativo")
        return oggetto


class BombaAcida(Oggetto):
    """
    Infligge danno pari al valore(Proprietà)
    """
    def __init__(
        self,
        nome: str = "Bomba Acida",
        valore: int = 30,
        tipo_oggetto: str = "Offensivo"
        ) -> None:
        """
        Inizializza una bomba acida

        Args:
            nome (str): Nome della bomba
            danno (int): Danno inflitto dalla bomba (dafault: 30)

        Returns:
            None
        """
        super().__init__(nome=nome, valore=valore, tipo_oggetto=tipo_oggetto)

    def usa(self, mod_ambiente: int = 0) -> int:
        """
        Infligge danno al bersaglio
        !!!ATTENZIONE!!!
        Il valore viene passato come un valore negativo!

        Args:
            mod_ambiente (int): variabile dell'Ambiente in cui si trova l'oggetto

        Returns:
            int: Danno inflitto dalla bomba
        """
        self.usato = True
        return - (self.valore + mod_ambiente)

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        data = super().to_dict()
        return data


    @classmethod
    def from_dict(cls, data: dict) -> "BombaAcida":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        oggetto = cls(nome=data["nome"])
        oggetto.usato = data.get("usato", False)
        oggetto.valore = data.get("valore", 30)
        oggetto.tipo_oggetto = data.get("tipo_oggetto", "Offensivo")
        return oggetto


class Medaglione(Oggetto):
    """
    Incrementa l'attacco_max del personaggio che lo usa
    """
    def __init__(self,
                 nome: str = "Medaglione",
                 valore: int = 10,
                 tipo_oggetto: str = "Supporto") -> None:
        """
        Inizializza un medaglione

        Args:
            None

        Returns:
            None
        """
        super().__init__(nome=nome, valore=valore, tipo_oggetto=tipo_oggetto)

    def usa(self, mod_ambiente: int = 0) -> None:
        """
        Incrementa l'attacco_max del personaggio che lo usa

        Args:
            mod_ambiente (int): variabile dell'Ambiente in cui si trova l'oggetto

        Returns:
            None
        """

        self.usato = True
        return int(self.valore + mod_ambiente)

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """

        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict) -> "Medaglione":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        oggetto = cls(nome=data["nome"])
        oggetto.usato = data.get("usato", False)
        oggetto.valore = data.get("valore", 10)
        oggetto.tipo_oggetto = data.get("tipo_oggetto", "Supporto")
        return oggetto