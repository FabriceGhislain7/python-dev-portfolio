import random, uuid, logging
from dataclasses import dataclass, field


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# ogni logger del logging ha un livello di soglia ed i messaggi vengono inviati
# solo se il livello è maggiore di quello di soglia
# i livelli standard (in ordine crescente di gravità): DEBUG, INFO, ERROR, CRITICAL
# quindi facendo logger.setLevel(logging.INFO) i messaggi di livello inferiore
# ad info vengono ignorati
# in produzione si alza la soglia almeno a warning in modo da non intasare il
# log con troppi messaggi


@dataclass
class Personaggio():
    """
    Classe Padre per tutte classi
    Contiene le proprietà comuni a ogni classe (Mago, Ladro, Guerriero)
    """
    nome: str = ""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    npc: bool = True
    salute: int = 100
    salute_max: int = 200
    attacco_min: int = 5
    attacco_max: int = 80
    storico_danni_subiti: list[int] = field(default_factory=list)
    livello: int = 1
    destrezza: int = 15
    classe: str = ""
    """
        in una @dataclass i campi possono avere un dato di default oppure
        possono avere dei dati calcolati al momento della creazione
        dell'istanza, tramite default_factory
        lambda è una funzione anonima che viene chiamata al momento della
        creazione di un nuovo oggetto in modo da generare il valore di default
        del campo id
        default_factory in pratica garantisce che ogni istanza abbia un
        proprio UUID unico, senza doverlo passare manualmente al costruttore
        Evita il problema di valori mutabili di default condivisi tra tutte
        le istanze (come succederebbe con una lista definita direttamente)
    """

    # def __init__(self, nome: str, npc: bool = True) -> None:
        # self.id = str(uuid.uuid4())
        # self.nome = nome
        # self.salute = 100
        # self.salute_max = 200
        # self.attacco_min = 5
        # self.attacco_max = 80
        # self.storico_danni_subiti = []
        # self.livello = 1
        # self.destrezza = 15  # Caratteristica per la sistema d20
        # self.npc = npc  # Indica se il personaggio è un NPC

    def esegui_azione(self) -> bool:
        """
        Tira un d20 e verifica se il risultato è minore o uguale alla destrezza del personaggio.

        Returns:
            bool: True se il testo è superato, False altrimenti.
        """
        tiro = random.randint(1, 20)
        successo = tiro <= self.destrezza
        if successo:
            msg = (
                f"{self.nome} ha eseguito l'azione con successo! (tiro={tiro})"
        )
            logger.info(msg)
        else:
            msg = f"{self.nome} ha fallito l'azione! (tiro={tiro})"
            logger.info(msg)
        return successo

    def attacca(self, mod_ambiente: int = 0) -> int:
        """
        Tenta un attacco generando un danno casuale tra attacco_min e attacco_max,
        influenzato da eventuali modificatori ambientali. Il successo dipende da un tiro
        basato sulla destrezza (sistama d20).

        Args:
            mod_ambiente (int): modificatore di attacco in base all'ambiente

        Returns:
            int: danno inflitto all'avversario, 0 se l'attacco fallisce
        """
        danno = 0
        if self.esegui_azione():
            danno = random.randint(self.attacco_min, self.attacco_max) + mod_ambiente
            msg = f"{self.nome} Attacca con successo e infligge {danno} danni!"
        else:
            msg = f"{self.nome} Tenta di attaccare ma fallisce!"
        logger.info(msg)
        return danno

    def subisci_danno(self, danno: int) -> None:
        """
        Sottrae il danno (Input) alla salute del personaggio.
        Args:
            danno (int): danno subito dal personaggio
        """
        self.salute = max(0, self.salute - danno)
        self.storico_danni_subiti.append(danno)
        msg = f"Salute di {self.nome}: {self.salute}\n"
        logger.info(msg)

    def sconfitto(self) -> bool:
        """
        Verifica se il personaggio è sceso a zero di salute.
        Returns:
            bool: True se il personaggio è sconfitto, in caso contrario False
        """
        return self.salute <= 0

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        """
        Recupera la salute del personaggio del 30% della salute corrente.
        Viene usato da pozioni e dal recupero salute post duello.

        Args:
            mod_ambiente (int): modificatore di recupero in base all'ambiente
        """
        if self.salute >= self.salute_max:
            msg = f"{self.nome} ha già la salute piena."
            logger.info(msg)
            return
        recupero = int(self.salute * 0.3) + mod_ambiente
        nuova_salute = min(self.salute + recupero, 100)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = (
            f"\n{self.nome} recupera {effettivo} HP."
            f" Salute attuale: {self.salute}"
        )
        logger.info(msg)

    def migliora_statistiche(self) -> None:
        """
        Metodo per aumentare il livello del personaggio e quindi
        migliorarne le statistiche.
        Aumenta del 2% l'attacco massimo e dell'1% la salute massima.
        """
        self.livello += 1
        self.attacco_max = int(self.attacco_max + 0.02 * self.attacco_max)
        self.salute_max = int(self.salute_max + 0.01 * self.salute_max)
        msg = f"{self.nome} è salito al livello {self.livello}!"
        logger.info(msg)