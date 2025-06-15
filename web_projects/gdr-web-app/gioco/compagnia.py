from gioco.personaggio import Personaggio
from gioco.classi import Guerriero, Mago, Ladro
from gioco.oggetto import Oggetto, PozioneCura, BombaAcida, Medaglione
from gioco.inventario import Inventario
from gioco.menu_principale import MenuPrincipale

class Compagnia:
    """
    Gestisce i personaggi del party e i loro inventari.

    Attributes:
        personaggi_inventari (list): Lista di tuple (Personaggio, Inventario).
        personaggi (list): Lista dei personaggi (solo oggetti Personaggio).
    """

    def __init__(self, menu_principale: MenuPrincipale) -> None:
        self.personaggi_inventari = menu_principale.personaggi_inventari
        self.personaggi = [pi[0] for pi in self.personaggi_inventari]

    def personaggi_presenti(self) -> list[str]:
        """
        Restituisce i nomi e le classi dei personaggi presenti nella compagnia.

        Returns:
            list[str]: Descrizioni dei personaggi.
        """
        return [f"Nome: {p.nome}, Classe: {p.__class__.__name__}" for p in self.personaggi]

    def aggiungi_personaggio(self, personaggio_inventario: tuple[Personaggio, Inventario]) -> None:
        """
        Aggiunge un personaggio e il suo inventario.
        """
        self.personaggi_inventari.append(personaggio_inventario)
        self.personaggi.append(personaggio_inventario[0])

    def rimuovi_personaggio(self, personaggio: Personaggio) -> bool:
        """
        Rimuove un personaggio (e il suo inventario) dalla compagnia.

        Returns:
            bool: True se rimosso, False se non trovato.
        """
        if personaggio in self.personaggi:
            self.personaggi_inventari = [
                pi for pi in self.personaggi_inventari if pi[0] != personaggio
            ]
            self.personaggi.remove(personaggio)
            return True
        return False

    def mostra_inventari(self) -> dict:
        """
        Restituisce tutti gli inventari dei personaggi.

        Returns:
            dict: {nome_personaggio: [nomi_oggetti]}
        """
        inventari_dict = {}
        for personaggio, inventario in self.personaggi_inventari:
            inventari_dict[personaggio.nome] = [obj.nome for obj in inventario.oggetti]
        return inventari_dict

    def get_inventari(self) -> list[Inventario]:
        return [inv for _, inv in self.personaggi_inventari]

    def get_personaggi_inventari(self) -> list[tuple[Personaggio, Inventario]]:
        return self.personaggi_inventari
