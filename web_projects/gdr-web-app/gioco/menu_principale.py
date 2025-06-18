from utils.salvataggio import Json, SerializableMixin
from gioco.personaggio import Personaggio
from gioco.classi import Guerriero, Ladro, Mago
from gioco.inventario import Inventario
from gioco.oggetto import Oggetto, PozioneCura, BombaAcida, Medaglione
from gioco.ambiente import Ambiente
from gioco.missione import Missione
from utils.salvataggio import SerializableMixin
import os

# ======================= VERSIONE PROVISORIA ===================================
@SerializableMixin.register_class
class MenuPrincipale(SerializableMixin):
    """
    Gestisce il menu principale del gioco, inclusa la creazione di nuovi personaggi,
    il caricamento di giochi salvati e la generazione degli inventari iniziali.
    """

    def __init__(self)-> None:
        """
        Inizializza una nuova istanza della classe Menu.

        Args:
            None

        Attributes:
            giocatore (None): Riservato per eventuale giocatore principale (non ancora utilizzato).
            personaggi (list): Lista dei personaggi creati o caricati.
            inventari (list): Lista degli inventari associati ai personaggi.
            personaggi_inventari (list): Lista di tuple (Personaggio, Inventario).

        Returns:
            None
        """
        self.giocatore = None
        self.personaggi = []
        self.inventari = []
        self.personaggi_inventari = []
        self.nemici = []
        self.ambiente = None
        self.missione = None
    def mostra_menu(self) -> None:
        """
        Mostra il menu principale all'utente per scegliere tra un nuovo gioco(1)
        o il caricamento di un gioco salvato(2).

        Args:
            None

        Returns:
            None
        """
        opzioni = ["1"]
        if os.path.exists("data/salvataggio.json"):
            opzioni.append("2")
        scelta = IU.chiedi_input("1: Nuovo Gioco\n" + ("2: Gioco Salvato\n" if "2" in opzioni else "") + "Scegli: ", opzioni=opzioni)
        if scelta == "1":
            self.crea_nuovo_salvataggio()
        if scelta == "2":
            self.carica_salvataggio()

    def crea_nuovo_salvataggio(self)-> None:
        """
        Avvia una nuova partita chiedendo all'utente quanti personaggi creare.
        Per ogni personaggio creato viene generato un inventario iniziale.
        """
        if os.path.exists("data/salvataggio.json"):
            os.remove("data/salvataggio.json")
        num_personaggi = IU.chiedi_numero("Quanti personaggi vuoi creare? : ", minimo=1)
        for _ in range(num_personaggi):
            personaggio = self.crea_personaggio()
            self.personaggi.append(personaggio)
            zaino_personaggio = self.crea_inventario(personaggio)
            self.inventari.append(zaino_personaggio)
            self.personaggi_inventari.append((personaggio, zaino_personaggio))

    def carica_salvataggio(self) -> None:
        dati = Json.carica_dati("data/salvataggio.json")
        if dati is None:
            print("Errore nel caricamento del salvataggio.")
            return

        self.personaggi_inventari = []
        self.nemici = []

        personaggi_dati = dati.get("personaggi", [])
        inventari_dati = dati.get("inventari", [])

        if len(personaggi_dati) != len(inventari_dati):
            print("Attenzione: numero di personaggi e inventari non corrispondono.")

        # 1. Crea una mappa nome → personaggio, deserializzando solo una volta
        personaggi = []
        mappa_pg = {}
        for pg_dict in personaggi_dati:
            pg = SerializableMixin.from_dict(pg_dict)
            mappa_pg[pg.nome] = pg
            personaggi.append(pg)

        # 2. Deserializza inventari collegando il proprietario già esistente
        for i, inv_dict in enumerate(inventari_dati):
            inv = SerializableMixin.from_dict(inv_dict)
            proprietario_dict = inv_dict.get("proprietario", {})
            nome_proprietario = proprietario_dict.get("nome")

            if nome_proprietario in mappa_pg:
                inv.proprietario = mappa_pg[nome_proprietario]
                self.personaggi_inventari.append((mappa_pg[nome_proprietario], inv))
            else:
                print(f"Proprietario '{nome_proprietario}' non trovato tra i personaggi.")
                self.personaggi_inventari.append((None, inv))

        # 3. Carica nemici e i loro inventari
        nemici_dati = dati.get("nemici", [])
        inventari_nemici_dati = dati.get("inventari_nemici", [])

        if len(nemici_dati) != len(inventari_nemici_dati):
            print("Attenzione: numero di nemici e inventari nemici non corrispondono.")

        for i, nem_dict in enumerate(nemici_dati):
            personaggio = SerializableMixin.from_dict(nem_dict.get("personaggio", {}))
            inventario = SerializableMixin.from_dict(inventari_nemici_dati[i]) if i < len(inventari_nemici_dati) else None
            strategia_attacco = None  # TODO: deserializza strategia se presente in futuro
            self.nemici.append((personaggio, strategia_attacco, inventario))

        # 4. Carica gestore missioni
        gestore_missioni_dict = dati.get("gestore_missioni") or dati.get("missioni")
        if gestore_missioni_dict:
            self.gestore_missioni = SerializableMixin.from_dict(gestore_missioni_dict)
        else:
            print("Nessun dato missioni trovato nel salvataggio.")
            self.gestore_missioni = None




    print("Salvataggio caricato correttamente.")
    def crea_personaggio(self) -> Personaggio:
        """
        Crea un nuovo personaggio tramite input utente.

        Args:
            None

        Returns:
            Personaggio(object): L'istanza del personaggio creato.
        """
        print("Crea un nuovo personaggio\n")
        pg_name = IU.chiedi_input("Nome del personaggio : ")
        classi_disponibili = [Ladro, Guerriero, Mago]
        for indx, classe in enumerate(classi_disponibili, start=1):
            print(f"{indx}- {classe.__name__}")
        idnx_pg_classe = IU.chiedi_numero("Classe del personaggio : ", minimo=1, massimo=len(classi_disponibili))
        pg = classi_disponibili[idnx_pg_classe - 1](pg_name)
        return pg

    def crea_inventario(self, pg: Personaggio = None) -> Inventario:
        """
        Crea un inventario iniziale per un personaggio e permette di scegliere un oggetto iniziale.

        Args:
            pg (Personaggio, optional): Il personaggio a cui assegnare l'inventario.

        Returns:
            Inventario(object): L'inventario creato con l'oggetto iniziale selezionato.
        """
        zaino = Inventario(proprietario=pg)
        print("Cominci la tua avventura con un :")
        oggetti_disponibili = [PozioneCura, BombaAcida, Medaglione]
        for indx, obj in enumerate(oggetti_disponibili, start=1):
            print(f"{indx}- {obj.__name__}")
        indx_initial_gift = IU.chiedi_numero("Scegli :", minimo=1, massimo=len(oggetti_disponibili))
        zaino.aggiungi(oggetti_disponibili[indx_initial_gift - 1]())
        return zaino